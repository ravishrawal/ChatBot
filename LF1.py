import json
import boto3


def queue_message(msgDetails):
    #create sqs client 
    
    sqs = boto3.client('sqs')
    queue_url = 'https://sqs.us-east-1.amazonaws.com/492808346955/DinnerSpecs'
    
    #send message to sqs queue
    
    sqs_msg_attr = {}
    for key,val in msgDetails.items():
        sqs_msg_attr[key] = {'DataType': 'String', 
                      'StringValue': val}
            
    sqs_response = sqs.send_message(
            QueueUrl = queue_url,
            DelaySeconds = 10,
            MessageAttributes = sqs_msg_attr,
            MessageBody = ('Dinner Specs'),
        )
    print('sqs_response:  ', sqs_response['MessageId'])
    
    
#Initialise outgoing message
outgoing_response = {}

#Take user input, check intent, format reponse
def lambda_handler(event, context):

    response_message_content = ''
    #Which intent?
    if event['currentIntent']['name'] == 'greetingIntent':
        response_message_content = 'Welcome, how can I help you?'
        
    elif event['currentIntent']['name'] == 'dinnerSuggestions':
        dinnerDetails = event['currentIntent']['slots']
        response_message_content = f"Ah, so you want {dinnerDetails['Cuisine']} in {dinnerDetails['Location']} at {dinnerDetails['DiningTime']}. {dinnerDetails['NumberOfPeople']} people. We're texting you five recommendations at {dinnerDetails['PhoneNumber']}!"
        
        queue_message(dinnerDetails)
        
    elif event['currentIntent']['name'] == 'thankyouIntent':
        response_message_content = 'You\'re Welcome!'
        
        
    outgoing_response["dialogAction"] = {
            "type": "ElicitIntent",
            "message": {
                "contentType": "PlainText",
                "content": response_message_content
            },
        }
        
      
    return outgoing_response
