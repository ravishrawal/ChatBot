import boto3
from boto3.dynamodb.conditions import Key, Attr
import datetime
class mydb():
    def __init__(self, table_name):
        self.table_name = table_name
        # Get the service resource.
        # Create or load table
        dynamodb = boto3.resource('dynamodb')
        try:
            self.table = self.create()
        except:
            self.table = dynamodb.Table(table_name)



    def create(self):
        # Create the DynamoDB table
        print(f'creating table {self.table_name}')
        dynamodb = boto3.resource('dynamodb')
        print(dynamodb)
        table = dynamodb.create_table(
            TableName=self.table_name,
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'insertedAtTimestamp',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'insertedAtTimestamp',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 50,
                'WriteCapacityUnits': 50
            }
        )
        print("whats happening?")
        # Wait until the table exists
        table.meta.client.get_waiter('table_exists').wait(TableName=self.table_name)
        print("got to waiting")
        return table


    def write(self, restaurantList):
        with self.table.batch_writer() as batch:
            for restaurant in restaurantList:
                now = datetime.datetime.now()
                restaurant["insertedAtTimestamp"] = now.strftime("%Y-%m-%d %H:%M:%S")
                batch.put_item(restaurant)

    # # Print out some data about the table.
    # print(table.creation_date_time)
    # print("item count:", table.item_count)



    def query(self, dinnerSpecs):
        response = table.scan(
            Attr('location.city').eq(dinnerSpecs["location"]) & 
            Attr('cuisine').eq(dinnerSpecs["cuisine"])
            )
        response_items = response['Items']
        print("response_item_first_5",response_item[:5])
        return response_items[:5]
