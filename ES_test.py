from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch.helpers import bulk,parallel_bulk
from collections import deque
from requests_aws4auth import AWS4Auth
import boto3
import requests

host = "search-restaurants-ythkwzbi6a5lpqmuchwqxbrpyy.us-east-1.es.amazonaws.com"
region = 'us-east-1' # e.g. us-west-1
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key,
								region, service, session_token=credentials.token)

es = Elasticsearch(
			hosts=[{'host': host, 'port': 443}],
			http_auth = awsauth,
			use_ssl = True,
			verify_certs=True,
			connection_class = RequestsHttpConnection
			)