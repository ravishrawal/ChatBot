import requests
import json

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
	res = json.loads(response.text)

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
			output_list.append(data)
		except:
			print('this one failed')
			
	return output_list


# Use Get Req
cuisine = 'mexican'
location = 'manhattan'

search_params = {
	"categories": cuisine,
	"location": location,
	"limit": 50,
}

output = yelp_get(search_params)
print(len(output))
