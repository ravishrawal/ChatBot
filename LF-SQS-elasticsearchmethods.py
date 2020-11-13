from elasticsearch import Elasticsearch, RequestsHttpConnection
import boto3
from requests import *
import sys
sys.path.insert(1, '/opt')
from requests_aws4auth import AWS4Auth


class MyES():
    def __init__(self):
        self.host = "search-restaurants-ythkwzbi6a5lpqmuchwqxbrpyy.us-east-1.es.amazonaws.com"
        self.region = 'us-east-1' # e.g. us-west-1
        self.service = 'es'
        self.credentials = boto3.Session().get_credentials()
        self.awsauth = AWS4Auth(self.credentials.access_key, self.credentials.secret_key,
                                self.region, self.service, session_token=self.credentials.token)
    
    def connect(self):
        self.es = Elasticsearch(
            hosts=[{'host': self.host, 'port': 443}],
            http_auth = self.awsauth,
            use_ssl = True,
            verify_certs=True,
            connection_class = RequestsHttpConnection
            )

        return self.es
        
def queryES(cuisine):
    ES = MyES()
    ES_connect = ES.connect()
    print('ES connected')
    key, value = "cuisine", cuisine
    es_response = ES_connect.search(index="restaurants", 
                        body={
                            "query": { 
                                "match": {
                                    key: value
                                }
                            }
                        })
    es_res = es_response['hits']['hits'] 
    restaurant_ids = [item['_source']['restaurantId'] for item in es_res]
    print('restaurantIds', restaurant_ids)
    return restaurant_ids