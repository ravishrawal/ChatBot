import json
import boto3



def receive_and_delete_msg(records):
    # TODO handle multiple records
    sqs = boto3.client('sqs')
    for record in records:
        rec_split = record["eventSourceARN"].split(":")
        id = rec_split[4]
        queue_name = rec_split[5]
        # URL looks like this: https://sqs.us-east-1.amazonaws.com/492808346955/DinnerSpecs 
        queue_url = "https://sqs." + record["awsRegion"] + ".amazonaws.com/" + id + "/" +  queue_name
        receipt_handle = record["ReceiptHandle"]
        # Delete message from queue
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle)
        return record["messageAttributes"]

def lambda_handler(event, context):
    # TODO implement
    dinnerDetails = receive_and_delete_msg(event["Records"])
    print(dinnerDetails)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
