# Introduction
A Python script to fetch the top sites from for a particular country. It uses AWS Alexa Top Sites Service, so you have to register a AWS account before using.


# Requirements
- Python 2 or Python 3
- Needed libraries can be installed by the following command

```$python
pip install -r requirements.txt
```

# Usage
```$shell
./ats.py -country US -count 1000 -secret xxx -key xxx [-start 10]
```

Where:
- country: should be the 2 character [ISO_3166-1 style] (http://en.wikipedia.org/wiki/ISO_3166-1)
- count: the number of top sites to fetch
- secret: secret access key from your AWS account
- key: access key id from your AWS account
- start(optional): the website ranking you want to get started, the default is 1

Results will be:
- printed to the screen with format: `Ranking Domain`
- saved to a json file (top_alexa.json) with format `{"1": "google.com", ...}`

# References
[1] https://docs.aws.amazon.com/AlexaTopSites/latest/

[2] https://aws.amazon.com/alexa-top-sites/