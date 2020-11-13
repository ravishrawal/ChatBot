# Chatbot Concierge #

## About ##

A dinner recommendation chatbot which uses ASR & NLU through AWS Lex to conversationally receive user information and send a text message with restaurant suggestions to your phone. Built on a cloud stack (AWS S3, DynamoDB, ElasticSearch, Lambda, SQS, SNS, API gateway, Lex) with a little help from the Yelp API. 


### Authors ###
1. Ravish Rawal
2. Viren Bajaj

## Usage ##
Chat with the bot to get dining recommendations in NYC: 
http://cloud-chatbot-rav-viren.s3-website-us-east-1.amazonaws.com/


## Lambda Functions ##
1. LF0 - interfaces between the user and Lex
2. LF1 - pushes user specifications to SQS
3. LF-SQS (LF2) - triggers on message(s) received by SQS, queries DBs, sends user text message with recommendations.

## Helper Scripts ##
1. yelp_scraper.py - used to scrape yelp for restaurants and populate dyanmo DB and elastic search
2. dyanamodb.py - helper class that interfaces with dynamodb table
3. elastic_search.py - helper class that interfaces with elastic search
4. yelp_example.py - sample response from yelp search API

## API ##
1. AI Customer Service API-test-swagger-apigateway.yaml
