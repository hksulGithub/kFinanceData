import requests
import re
import os
import zipfile
import tempfile
import pandas as pd
import datetime

from pytz import timezone

import requests
import json

        
class kFinanceDataInstance:

  def __init__(self, APP_KEY, APP_SECRET ):
    self._APP_KEY = APP_KEY
    self._APP_SECRET = APP_SECRET
    self._AUTH_PATH = "oauth2/tokenP"
    self._URL_BASE = "https://openapivts.koreainvestment.com:29443"
    self._FUTURESOPTIONS_PRICE_URL = "/uapi/domestic-futureoption/v1/quotations/inquire-price"
    self._codeDataFrame = self._getFutureOptionCodes()

  def genAuthToken(self):
    headers = {"content-type":"application/json"}
    body = {"grant_type":"client_credentials",
            "appkey":self._APP_KEY, 
            "appsecret":self._APP_SECRET}
    
    URL = f"{self._URL_BASE}/{self._AUTH_PATH}"
    res = requests.post(URL, headers=headers, data=json.dumps(body))
    try:
      self._ACCESS_TOKEN = res.json()["access_token"]
      print(self._ACCESS_TOKEN)
    except:
      print("genAuthToken Error", res.json())
    

  def useAuthToken(self, newToken):
    self._ACCESS_TOKEN = newToken

  def _getFutureOptionCodesHeaderData(self):
    zipFileInfoUrl = "https://raw.githubusercontent.com/koreainvestment/open-trading-api/main/stocks_info/domestic_future_code.py"
    responseText = requests.get(zipFileInfoUrl).text
    zipFileInfoPattern = r"urllib.request.urlretrieve\(\"([^\"]*)\""
    match = re.search(zipFileInfoPattern, responseText)
    actualZipFileUrl = match.group(1)
    startIndex = responseText.find("[")
    endIndex = responseText.rfind("]")
    zipFileColumnData = eval(responseText[startIndex:endIndex+1])
    zipFileColumnData = [a.strip() for a in zipFileColumnData]
    return (actualZipFileUrl, zipFileColumnData)

  def _getFutureOptionCodesFromZipUrlandColumns(self, zipFileUrl, zipFileColumns):
    r = requests.get(zipFileUrl)
    with tempfile.TemporaryDirectory() as tmp_dir:
      zip_file_path = os.path.join(tmp_dir, 'fo_idx_code_mts.zip')
      with open(zip_file_path, "wb") as f:
        f.write(r.content)
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
          zip_ref.extractall(tmp_dir)
          mst_file_path = os.path.join(tmp_dir, "fo_idx_code_mts.mst")
          codeDF = pd.read_csv(mst_file_path, delimiter='|', encoding='CP949', names=zipFileColumns, header=None)
          return codeDF
    return None


  def _getFutureOptionCodes(self):
    zipUrl, zipFileColumns = self._getFutureOptionCodesHeaderData()
    return self._getFutureOptionCodesFromZipUrlandColumns(zipUrl, zipFileColumns)
  
  def getFutureOptionCodes(self):
    return self._codeDataFrame
  
  def downloadFuturesOptions(self, futureOptionsCodeList):

    FutureOptions_Price_URL = f"{self._URL_BASE}/{self._FUTURESOPTIONS_PRICE_URL}"
    inputHeaders = {#"Content-Type":"application/json", 
              "content-type":"utf-8",
              "authorization": f"Bearer {self._ACCESS_TOKEN}",
              "appKey":self._APP_KEY,
              "appSecret":self._APP_SECRET,
              "custtype":"P"
              }
    inputHeaders["tr_id"] = "FHMIF10000000"
    
    if len(futureOptionsCodeList) <1:
      return None
    else:
      for i, code in enumerate(futureOptionsCodeList):
        if i == 0:
          df = self.getSingleDataFrame(code, FutureOptions_Price_URL, inputHeaders)
        else:
          df_new = self.getSingleDataFrame(code, FutureOptions_Price_URL, inputHeaders)
          df = pd.concat([df, df_new])
      return df

  def convertShortCodeToType(self, shortCode):
    distinct_values = self._codeDataFrame.loc[self._codeDataFrame['단축코드'] == shortCode, '상품종류'].unique()
    if len(distinct_values) == 1:
      return self.convertShortCodeTypeToKISValue(distinct_values[0])
    else:
      return None

  def convertShortCodeTypeToKISValue(self, shortCodeType):
    if shortCodeType in ('1'):
      return 'F'
    elif shortCodeType in ('5', '6'):
      return 'O'

  def getSingleDataFrame(self, code, url, header):
    param = {
      "fid_input_iscd": code,
      "fid_cond_mrkt_div_code": self.convertShortCodeToType(code)
    }
    now = datetime.datetime.now(timezone('Asia/Seoul'))
    res = requests.get(url, headers=header, params=param)
    output = res.json()
    try:
      df_one = pd.DataFrame(output['output1'], index=[0])
      df_one.insert(0, 'date', now.strftime("%Y%m%d"))
      df_one.insert(1, 'time', now.strftime("%H:%M") )
      df_one.insert(2, 'kospi200Index', output['output3']['bstp_nmix_prpr'])
      
      typeValue = ""
      if df_one['hts_kor_isnm'].iloc[0][0] in ('C', 'P'):
        typeValue = df_one['hts_kor_isnm'].iloc[0][0]
      elif df_one['hts_kor_isnm'].iloc[0][0] in ['F']:
        typeValue = "F"
      df_one.insert(3, 'type', typeValue)

      maturity = ''
      exercisePrice = ''
      if typeValue in ('C', 'P'):      
        maturity, exercisePrice = df_one['hts_kor_isnm'].iloc[0].split()[1:]
      elif typeValue in ('F'):
        maturity = df_one['hts_kor_isnm'].iloc[0].split()[1]

      df_one.insert(4, 'maturity', maturity)
      df_one.insert(5, 'exercisePrice', exercisePrice)

      df_one.insert(6, 'price', df_one.pop('futs_prpr'))
      return df_one
    except:
      if output.msg_cd == "EGW00123":
        print ("Auth Token expired. Must be reissued")
      print("Error, getSingleDataframe: res", output)
    


