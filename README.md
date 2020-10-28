# Chatbot Concierge #

## About ##

HW 1 of the Cloud Computing & Big Data class at Columbia University and New York University.


### Authors ###
1. Ravish Rawal (rr2914)
2. Viren Bajaj (vb2519)

## Usage ##
Chat with the bot to get dining recommendations in NYC: 
https://cloud-chatbot-rav-viren.s3.amazonaws.com/chat.html


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
