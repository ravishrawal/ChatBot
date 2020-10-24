import json
import boto3

def sendToLex(event):
    client = boto3.client('lex-runtime')
    
    #get IP address for unique user ID
    user_id = event['requestContext']['identity']['sourceIp']
    
    #get user input
    data = json.loads(event['body'])
    msg_in = data['messages'][0]['unstructured']['text']
    
    #send input to lex
    lex_response = client.post_text(
        botName = 'ChatBot',
        botAlias = 'Dev',
        userId = user_id,
        inputText = msg_in,
    )
    
    return lex_response

def lambda_handler(event, context):
    #send to Lex, get response
    lex_response = sendToLex(event)
    
    #send response back to user
    print(lex_response)
    print(lex_response['message'])
    message_out = {   'messages':
                      [{
                      'type': 'unstructured',
                      'unstructured': {
                          #INSERT LEX RESPONSE HERE
                          'text': lex_response['message']
                          }
                      }]
              }
    
    
    return {
        'statusCode': 200,
        'headers': {   
            'Access-Control-Allow-Origin': '*'
        }, 
        'body': json.dumps(message_out)
        }