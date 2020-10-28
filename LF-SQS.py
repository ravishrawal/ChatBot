import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import logging



def receive_and_delete_msg(records):
    #TODO handle multiple records
    sqs = boto3.client('sqs')
    results = []
    for record in records:
        rec_split = record["eventSourceARN"].split(":")
        id = rec_split[4]
        queue_name = rec_split[5]
        # URL looks like this: https://sqs.us-east-1.amazonaws.com/492808346955/DinnerSpecs 
        queue_url = "https://sqs." + record["awsRegion"] + ".amazonaws.com/" + id + "/" +  queue_name
        receipt_handle = record["receiptHandle"]
        # Delete message from queue
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle)
        results.append(record["messageAttributes"])
    return results
    

def query_db(dinnerSpecs):
    # Get dynamo db object
    dynamodb = boto3.resource('dynamodb')
    table_name = 'yelp-restaurants'
    table = dynamodb.Table(table_name)
    # db.table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    location = dinnerSpecs['Location'].title()
    cuisine = dinnerSpecs['Cuisine']
    print(location,cuisine)
    results =  table.scan(FilterExpression = 
                    Attr('cuisine').eq(cuisine) & 
                    Attr('location.city').eq(location))
    print(len(results['Items']))
    return results['Items'][:5]

def send_text(results,spec):
    # Initialize logger and set log level
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Initialize SNS client for Ireland region
    session = boto3.Session(
        region_name="us-east-1"
    )
    sns_client = session.client('sns')
    if len(results) > 0:
        message = f"My recommendations for {spec['Cuisine']} for {spec['NumberOfPeople']} at {spec['DiningTime']}: \n"
        count = 1
        for r in results:
            message += f'{count}. ' + str(r["name"]) + ',\nAdress: ' + ' '.join(r["location"]["display_address"]) + ',\nPhone: ' + r["phone"] + '\n'
            count += 1
    else:
        message = 'Sorry, we could not find any restaurants that match your preferences.'
    phone = spec["PhoneNumber"]
    if phone[0]=='+' and len(phone)==12:
        num = phone
    else:
        num = '+1'+phone
    print(num,message)
    # Send message
    response = sns_client.publish(
        PhoneNumber=num,
        Message= message,
        MessageAttributes={
            'AWS.SNS.SMS.SenderID': {
                'DataType': 'String',
                'StringValue': 'SENDERID'
            },
            'AWS.SNS.SMS.SMSType': {
                'DataType': 'String',
                'StringValue': 'Promotional'
            }
        }
    )

    logger.info(response)

def parse_details(dinnerDetails):
    specs = []
    for record in dinnerDetails:
        spec = {}
        spec['Location'] = record["Location"]["stringValue"] 
        spec['Cuisine'] = record["Cuisine"]["stringValue"]
        spec['PhoneNumber'] = record["PhoneNumber"]["stringValue"]
        spec['NumberOfPeople'] = record["NumberOfPeople"]["stringValue"]
        spec['DiningTime'] = record["DiningTime"]["stringValue"]
        specs.append(spec)
    return specs

def lambda_handler(event, context):
    # TODO implement
    print(event)
    dinnerDetails = receive_and_delete_msg(event["Records"])
    # dinnerDetails = event["Records"]["dinnerSpecs"]
    dinnerSpecs = parse_details(dinnerDetails)
    for spec in dinnerSpecs:
        results = query_db(spec)
        send_text(results,spec)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
