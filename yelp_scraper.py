import requests
import json
import time
import dynamodb as dydb
from decimal import Decimal
from boto3.dynamodb.conditions import Key, Attr

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
db = dydb.mydb(table_name)
# db.table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
print(db.table.creation_date_time)

populate = True 

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
			# db.write(output)
			for restaurant in output:
				db.table.delete_item(Key = {'id': restaurant["id"]}, ConditionExpression = Attr('cuisine').not_exists())

print("item count:", len(db.table.scan()))







