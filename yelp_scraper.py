import requests
import json
import time
import dynamodb as dydb
from decimal import Decimal
from boto3.dynamodb.conditions import Key, Attr
import elastic_search
url = 'https://api.yelp.com/v3/businesses/search'

API_KEY = 'W6x38pcDKTCTwHr7PSN8OPBjmqzmxFMiWYAqZajEe5_3aVH9fd-ts9B-y1Fg4bhh4-UFUZuJ9yptqwZbZExbg0oA0HxyIAK8n9u3dn8-Hof3L2HQ1VnvhATEA4OUX3Yx'

def yelp_get(params):
	#Auth
	headers = {
		"Authorization": "Bearer " + API_KEY
	}
	#Req
	response = requests.get(url, params = params, headers = headers)
	#Res
	res = json.loads(response.text,parse_float=Decimal)

	#Capture all results
	output_list = []
	restaurants = list(res.items())[0][1]
	#Loop restaurants, format for DB, append to output_list
	for restaurant in restaurants:
		try:
			data = {}
			data['id'] = restaurant['id']
			data['name'] = restaurant['name']
			data['location'] = restaurant['location']
			data['phone'] = restaurant['display_phone']
			data['rating'] = restaurant['rating']
			data['cuisine'] = params['categories']
			output_list.append(data)
		except:
			print('this one failed')			
	return output_list

# Get dynamo db object
table_name = 'yelp-restaurants'
DB = dydb.mydb(table_name)
# db.table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
print(DB.table.creation_date_time)

# response = DB.table.scan(FilterExpression = 
#                     Attr('cuisine').eq('american') &
#                     Attr('location.city').eq('New York'))
# print(response['Items'][:5])
# Create elastic search session
ES = elastic_search.myes()
# print(ES.awsauth)
# print(ES.es)
# ES.es.indices.create(index='restaurants')
# print(ES.es.indices.ping())
populate = False
dynamo = False
elasticsearch = False

if populate:
	cuisines = ['mexican', 'indian', 'chinese', 'italian', 'american']
	location = 'manhattan'

	for cuisine in cuisines:
		count = 0 
		while count < 1000:	
			search_params = {
				"categories": cuisine,
				"location": location,
				"limit": 50,
				"offset": count
			}	
			output = yelp_get(search_params)
			count += len(output)
			if dynamo:
				DB.write(output)
			if elasticsearch:
				ES.bulk_index(data=output)
			# break







