#!/usr/bin/python
import requests
import hmac
import argparse
import json
from hashlib import sha256
from datetime import datetime
from lxml import etree

AWS_REGION = "us-west-1"
AWS_SERVICE_NAME = "AlexaTopSites"
AWS_ALGORITHM = "AWS4-HMAC-SHA256"
AWS_TERMINATION = "aws4_request"
AWS_URI = "/api"
AWS_ACTION = "TopSites"
AWS_RESPONSE_GROUP = "Country"
AWS_ENDPOINT = "ats.us-west-1.amazonaws.com"
AWS_PREFIX_KEY = "AWS4"
AWS_MAX_COUNT = 1000
AWS_HOST = "ats.amazonaws.com"


class Helper:
    def __init__(self):
        pass

    """
    Some methods that the main program need
    """

    @staticmethod
    def sign(key, message, hex_digest=True):
        """
        Sign message with HMAC-SHA256
        :param key: secret key to sign
        :param message: message to sign
        :param hex_digest: If True, the signature is hex format; else the signature is bytes format
        """
        try:
            key.decode()
        except AttributeError:
            key = key.encode()
        except UnicodeDecodeError:
            pass

        if hex_digest:
            return hmac.new(key, msg=message.encode(), digestmod=sha256).hexdigest()
        return hmac.new(key, msg=message.encode(), digestmod=sha256).digest()

    @staticmethod
    def hash(message):
        """
        Hash the message by SHA256 algorithm
        """
        return sha256(message.encode()).hexdigest()


class AlexaTopSites:
    """
    The main class
    """

    def __init__(self, access_key_id, secret_access_key):
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.ranking = {}

    def get_sites(self, start, count, country_code, time_stamp, date_stamp):
        authorization_header = self.calc_auth_header(start, count, country_code, time_stamp, date_stamp)

        headers = {
            "Accept": "application/xml",
            "Content-Type": "application/xml",
            "x-amz-date": time_stamp,
            "Authorization": authorization_header
        }

        url = "https://%s%s?%s" % (AWS_HOST, AWS_URI, self.gen_query_string(start, count, country_code))

        r = requests.get(url, headers=headers)
        content = r.text
        ranking = self.parse(content)
        self.out(ranking)

    @staticmethod
    def gen_query_string(start, count, country_code):
        query = {
            "Action": AWS_ACTION,
            "ResponseGroup": AWS_RESPONSE_GROUP,
            "Start": start,
            "Count": count,
            "CountryCode": country_code
        }
        query_string = "&".join(["%s=%s" % (param, query[param]) for param in sorted(query)])
        return query_string

    def calc_auth_header(self, start, count, country_code, time_stamp, date_stamp):
        """
        Create an authorization header by signing multiple times.
        """

        headers = {
            "host": AWS_ENDPOINT,
            "x-amz-date": time_stamp
        }

        headers_list = ";".join([h for h in headers])
        headers_string = "\n".join(["%s:%s" % (param, headers[param]) for param in headers]) + "\n"

        query_string = self.gen_query_string(start, count, country_code)
        payload_hash = Helper.hash("")

        canonical_request = "\n".join(["GET", AWS_URI, query_string, headers_string, headers_list, payload_hash])
        hcr = Helper.hash(canonical_request)

        credential_scope = "/".join([date_stamp, AWS_REGION, AWS_SERVICE_NAME, AWS_TERMINATION])

        string_to_sign = "\n".join([AWS_ALGORITHM, time_stamp, credential_scope, hcr])

        signing_key = self.get_sign_key(date_stamp)

        signature = Helper.sign(signing_key, string_to_sign)
        authorization_header = "%s Credential=%s/%s, SignedHeaders=%s, Signature=%s" % (
            AWS_ALGORITHM, self.access_key_id, credential_scope, headers_list, signature)

        return authorization_header

    def get_sign_key(self, date_stamp):
        """
        Create a key to sign authorization string
        """
        key_date = Helper.sign(AWS_PREFIX_KEY + self.secret_access_key, date_stamp, hex_digest=False)
        key_region = Helper.sign(key_date, AWS_REGION, hex_digest=False)
        key_service = Helper.sign(key_region, AWS_SERVICE_NAME, hex_digest=False)
        key = Helper.sign(key_service, AWS_TERMINATION, hex_digest=False)
        return key

    @staticmethod
    def parse(content):
        """
        Convert the response of AWS to a dictionary.
        """
        ranking = {}
        xml = etree.fromstring(content)
        namespace_map = {'aws': 'http://ats.amazonaws.com/doc/2005-07-11'}
        entries = xml.xpath('//aws:Site', namespaces=namespace_map)
        for entry in entries:
            domain = entry.xpath('aws:DataUrl', namespaces=namespace_map)[0].text
            country = entry.xpath('aws:Country', namespaces=namespace_map)
            rank = country[0].xpath('aws:Rank', namespaces=namespace_map)[0].text
            ranking[int(rank)] = domain
        return ranking

    def out(self, ranking):
        """
        Print results to screen and save them to a file.
        """
        self.ranking.update(ranking)
        for r in ranking:
            print("%d %s" % (r, ranking[r]))
        with open('top_alexa.json', 'w') as outfile:
            json.dump(self.ranking, outfile)


def main():
    parser = argparse.ArgumentParser(description='Get a range of Alexa Top sites for a specific country')

    parser.add_argument('-key', action='store', dest='access_key_id', required=True)
    parser.add_argument('-secret', action='store', dest='secret_access_key', required=True)
    parser.add_argument('-country', action='store', dest='country_code', required=True)
    parser.add_argument('-count', action='store', dest='count', type=int, required=True)
    parser.add_argument('-start', action='store', dest='start', type=int)

    args = parser.parse_args()

    time_stamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    date_stamp = datetime.utcnow().strftime("%Y%m%d")

    access_key_id = args.access_key_id
    secret_access_key = args.secret_access_key
    country_code = args.country_code
    count = args.count
    start = args.start

    if count < 1:
        print("The number must be greater than 0.")
        exit(2)

    ats = AlexaTopSites(access_key_id, secret_access_key)
    if start is None:
        start = 1

    for i in range(int(count / AWS_MAX_COUNT)):
        ats.get_sites(start, AWS_MAX_COUNT, country_code, time_stamp, date_stamp)
        start += AWS_MAX_COUNT

    ats.get_sites(start, count % AWS_MAX_COUNT, country_code, time_stamp, date_stamp)


if __name__ == '__main__':
    main()
