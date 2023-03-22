# kfinancedata

A python library to access the Korean Financial Market Data Open API. (Currently only supported by 한국투자증권; KIS)^[https://apiportal.koreainvestment.com/]


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

pip install git+https://github.com/hksulGithub/kfinancedata.git


## Usage

from kfinancedata import kfinancedata as kf


### Examples


#### Sign In
```
 

APP_KEY = "YOUR_API_KEY"
APP_SECRET = "YOUR_API_SECRET" 


kf = kf.kfinancedataInstance(APP_KEY, APP_SECRET)
kf.genAuthToken()

```

##### Sign in using the Auth Token Previously Offered (KIS asks auth token to be reIssued once per day)
```

APP_KEY = "YOUR_API_KEY"
APP_SECRET = "YOUR_API_SECRET" 
issuedAuthToken = ""

kf = kf.kfinancedataInstance(APP_KEY, APP_SECRET)
kf.useAuthToken(issuedAuthToken)

```


#### Getting the List of Offered codes - Futures and Options

- Example: Get the list of Futures and options 
 - Matures in June
 - Is a Call option or a Put option on KOSPI200 index
 - And the Expiration price is between 290 and 330
```

expirationMonthString = "06" # June Maturity
assetTypeList = ('5', '6') # Is a Call option or a Put option on KOSPI200 index
exerciseLowerBound = 300
exerciseUpperBound = 320

kospi200DF = kf._codeDataFrame[(kf._codeDataFrame["기초자산 명"] == 'KOSPI200')]
kospi200OptionDF = kospi200DF[kospi200DF["상품종류"].isin(assetTypeList)] 
kospi200OptionPriceRangeDF = kospi200OptionDF[(kospi200OptionDF["행사가"]<exerciseUpperBound) & (kospi200OptionDF["행사가"]>exerciseLowerBound) ]
kospi200OptionPriceTimeRangeDF = kospi200OptionPriceRangeDF[kospi200OptionPriceRangeDF["단축코드"].str.slice(4,6) == nextMonthString]


codeList = list(kospi200OptionPriceTimeRangeDF['단축코드'])


```


#### Downloading the data into a dataframe

```
df = kf.downloadFuturesOptions(codeList) 
df

```

## Contributing


## License


### Acknowledgments

