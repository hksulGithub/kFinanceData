import sys
sys.path.append('./..')
from kFinanceData import kFinanceData as kfd
import datetime
import configparser


configFileDateFormat = '%Y-%m-%d %H:%M:%S'
config = configparser.ConfigParser()
config.read("./../../config.ini")

APP_KEY = config['auth']['APP_KEY']
APP_SECRET = config['auth']['APP_SECRET']

authTokenTimeString = config['token']['time']
autTokenDateTime = datetime.datetime.strptime(authTokenTimeString, configFileDateFormat)

print("authTokenTime", authTokenTimeString)
print("time passed since token issuance:", datetime.datetime.now()-autTokenDateTime)


kfdi = kfd.kFinanceDataInstance(APP_KEY, APP_SECRET)

if (datetime.datetime.now().date() == autTokenDateTime.date()):
  tokenString = config['token']['authToken']
  kfdi.useAuthToken(tokenString)
else:
  tokenString = kfdi.genAuthToken()
  print("new tokenstring", tokenString)
  if config.has_section('token')==False:
    config.add_section('token')
  nowString = datetime.datetime.now().strftime(configFileDateFormat)        
  config.set('token', 'time', nowString)
  config.set('token', 'authToken', tokenString)
  with open('./../../config.ini', 'w') as config_file:
      config.write(config_file)


expirationMonthString = "06" # June Maturity
assetTypeList = ('5', '6') # Is a Call option or a Put option on KOSPI200 index
exerciseLowerBound = 300
exerciseUpperBound = 320

codeDF = kfdi.getFutureOptionCodes()


codeDF = codeDF[(codeDF["기초자산 명"] == 'KOSPI200')]
codeDF = codeDF[codeDF["상품종류"].isin(assetTypeList)] 
codeDF = codeDF[(codeDF["행사가"]<exerciseUpperBound) & (codeDF["행사가"]>exerciseLowerBound) ]
codeDF = codeDF[codeDF["단축코드"].str.slice(4,6) == expirationMonthString]

codeList = list(codeDF['단축코드'])


print(codeList)


df = kfdi.downloadFuturesOptions(codeList) 


print(df)
