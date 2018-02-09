## Introduction
A Python script to fetch the top sites from for a particular country. It uses AWS Alexa Top Sites Service, so you have to register an AWS account before using.


## Requirements
- Python 2 or Python 3
- Needed libraries can be installed by the following command

```$python
pip install -r requirements.txt
```

## Usage
```$shell
./ats.py -country US -count 1000 -secret xxx -key xxx [-start 10]
```

Where:
- `country`: should be the 2 character [ISO_3166-1 style](http://en.wikipedia.org/wiki/ISO_3166-1)
- `count`: the number of top sites to fetch
- `secret`: secret access key from your AWS account
- `key`: access key id from your AWS account
- `start` (optional): the website ranking you want to get started, the default is 1

Results will be:
- printed to the screen with format: `Ranking Domain`
- saved to a json file (top_alexa.json) with format `{"1": "google.com", ...}`

## How to get an access key and a secret key

1. Sign up for an Amazon AWS account at [https://aws.amazon.com/](https://aws.amazon.com/).
2. [Create an IAM user](https://console.aws.amazon.com/iam/home?region=us-east-1#/users$new?step=details)
3. [Create a Customer Managed Policy](https://console.aws.amazon.com/iam/home?region=us-west-2#/policies$new?step=edit)
    - Select the JSON tab in the Policy Editor
    - If the following message box appears, you may safely close it. We are working to remove this false warning message.
        ![Policy](https://docs.aws.amazon.com/AlexaTopSites/latest/images/policy.jpg)

    - Paste the following in the editor window.
        ```json
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "AlexaTopSites:GET"
                    ],
                    "Resource": [
                        "*"
                    ]
                }
            ]
        }
        ```                       
    - Click Review Policy. In the Review Policy window, assign a Name to the policy and Click Create Policy.

    - The following warning message can be safely ignored.

        ![Policy Warning](https://docs.aws.amazon.com/AlexaTopSites/latest/images/polwarn1.jpg)

        ![Policy Warning](https://docs.aws.amazon.com/AlexaTopSites/latest/images/polwarn2.jpg)

4. Assign the previous execution policy for the service to the user created above.

5. Get the IAM access keys from the [IAM user management console page](https://console.aws.amazon.com/iam/home#/users) of the Amazon AWS portal.

## References
[1] https://docs.aws.amazon.com/AlexaTopSites/latest/

[2] https://aws.amazon.com/alexa-top-sites/

[3] https://secaholic.com/a-python-script-get-alexa-top-sites-4652768dfa96
