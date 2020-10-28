from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch.helpers import bulk,parallel_bulk
from collections import deque
from requests_aws4auth import AWS4Auth
import boto3
import requests



class myes():
	def __init__(self):
		self.host = "search-restaurants-ythkwzbi6a5lpqmuchwqxbrpyy.us-east-1.es.amazonaws.com"
		self.region = 'us-east-1' # e.g. us-west-1
		self.service = 'es'
		self.credentials = boto3.Session().get_credentials()
		self.awsauth = AWS4Auth(self.credentials.access_key, self.credentials.secret_key,
								self.region, self.service, session_token=self.credentials.token)
	
		self.es = self.connect()


	def connect(self):
		es = Elasticsearch(
			hosts=[{'host': self.host, 'port': 433}],
			http_auth = self.awsauth,
			use_ssl = True,
			verify_certs=True,
			connection_class = RequestsHttpConnection
			)
		return es


	def bulk_index(self,index_name='restaurants',data=[]):
		print('updating index ...')
		docs = []
		for elem in data:
			docs.append(
				{	
					'_op_type': 'index',
					'_index': index_name,
					'_id': elem['id'],
					'body': {'cuisine': elem['cuisine']}
				}
			)
		# print(docs[:2])
		# bulk(self.es,iter(docs),request_timeout=30)
		for success,info in parallel_bulk(self.es, iter(docs), request_timeout=30):
			if not success:
				print('A document failed:', info)
			else:
				print('success')

		if data==[]:
			print('no data provided')
		else:
			print('done')

