import os
import boto3
import requests
from requests_aws4auth import AWS4Auth

es_host = os.environ['ES_HOST']
es_index = "metadata"
es_type = "ourcompanies"
url = es_host + '/' + es_index + '/' + es_type + '/'

region = 'eu-west-1'
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

def index(event, context):
    print(event)
    for record in event['Records']:
        siren = str(record['dynamodb']['Keys']['siren']['S'])
        if record['eventName'] == 'REMOVE':
            res = requests.delete(url + siren, auth=awsauth)
        else:
            document = record['dynamodb']['NewImage']
            res = requests.put(url + siren, auth=awsauth, json=document, headers={"Content-Type": "application/json"})