import dynamodb as dydb
from boto3.dynamodb.conditions import Key, Attr

# Get dynamo db object
table_name = 'yelp-restaurants'
db = dydb.mydb(table_name)
# db.table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
print(db.table.creation_date_time)

response = db.table.scan(FilterExpression = Attr('cuisine').eq('indian'))
print(len(response['Items']))
# try:
# 	key = response['LastEvaluatedKey']
# except:
# 	key = None

# while key != None:
# 	try:
# 		key = response['LastEvaluatedKey']
# 	except:
# 		key = None
# 	response = db.table.scan(FilterExpression = Attr('cuisine').eq('indian'))
# 	print(len(response['Items']))

# for resp in response['Items'][:5]:
# 	print(resp['cuisine'])