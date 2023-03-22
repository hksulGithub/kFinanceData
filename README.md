# kFinanceData

A python library to access the Korean Financial Market Data Open API. (Currently only supported by 한국투자증권; KIS)^[https://apiportal.koreainvestment.com/]


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

pip install git+https://github.com/hksulGithub/kFinanceData.git


## Usage

```
from kFinanceData import kFinanceData as kf
```

### Examples


#### Sign In
```
 

APP_KEY = "YOUR_API_KEY"
APP_SECRET = "YOUR_API_SECRET" 


kf = kf.kFinanceDataInstance(APP_KEY, APP_SECRET)
kf.genAuthToken()

```

##### Sign in using previously issued Auth Token (KIS suggests auth token to be issued once per day)
```

APP_KEY = "YOUR_API_KEY"
APP_SECRET = "YOUR_API_SECRET" 
issuedAuthToken = "YOUR_AUTH_TOKEN"

kf = kf.kFinanceDataInstance(APP_KEY, APP_SECRET)
kf.useAuthToken(issuedAuthToken)

```


#### Getting the List of Offered codes - Futures and Options

- Example: Get the list of Futures and Options ...
  - That is a Call option or a Put option 
  - The underlying is the KOSPI200 Stock Index
  - That matures in June
  - And the Expiration price is between 300 and 320
  

```

assetTypeList = ('5', '6') # Is a Call option or a Put option on KOSPI200 index
expirationMonthString = "06" # June Maturity
exerciseBound = (300, 320)

kospi200DF = kf._codeDataFrame[(kf._codeDataFrame["기초자산 명"] == 'KOSPI200')]
kospi200OptionDF = kospi200DF[kospi200DF["상품종류"].isin(assetTypeList)] 
kospi200OptionPriceRangeDF = kospi200OptionDF[ (kospi200OptionDF["행사가"]<exerciseBound[1]) & (kospi200OptionDF["행사가"]>exerciseBound[0]) ]
kospi200OptionPriceTimeRangeDF = kospi200OptionPriceRangeDF[kospi200OptionPriceRangeDF["단축코드"].str.slice(4,6) == expirationMonthString]


codeList = list(kospi200OptionPriceTimeRangeDF['단축코드'])


```


#### Downloading the data into a dataframe

```
df = kf.downloadFuturesOptions(codeList) 
df

```

#### Sample Output

![](https://i.imgur.com/GJuMlwe.png)

## Contributing


## License


### Acknowledgments

