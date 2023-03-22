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

```
 

APP_KEY = "YOUR_API_KEY"
APP_SECRET = "YOUR_API_SECRET" 


kf = kf.kfinancedataInstance(APP_KEY, APP_SECRET)
kf.genAuthToken()



yourToken = ""
kf.useAuthToken(yourToken)
```

## Contributing


## License


### Acknowledgments

