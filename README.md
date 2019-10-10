# real-hackathon-backend

         ___        ______     ____ _                 _  ___  
        / \ \      / / ___|   / ___| | ___  _   _  __| |/ _ \ 
       / _ \ \ /\ / /\___ \  | |   | |/ _ \| | | |/ _` | (_) |
      / ___ \ V  V /  ___) | | |___| | (_) | |_| | (_| |\__, |
     /_/   \_\_/\_/  |____/   \____|_|\___/ \__,_|\__,_|  /_/ 
 ----------------------------------------------------------------- 


Lambda code for your APIWorld Hackathon 2019, use location based info and weather info to recommend activities to 

### URL to authenticate
https://o2k881hv2k.execute-api.us-west-1.amazonaws.com/dev_stage/auth

### Redirect URI
https://o2k881hv2k.execute-api.us-west-1.amazonaws.com/dev_stage/auth/redirect

## Inspiration
- AWS good serverless services can provide good support to our service.

## What it does
- This project provides a Serverless API for users to get up-coming activities and choose what they like. The data are from different sources, which can be selected by our clients.
 
## How we built it
- By using Lambda function, API gateway and DynamoDB, we transformed a server-based API to a Serverless API.
- We designed an algorithm to filter data and optimized it to run well on Lambda function.

## Challenges we ran into
- Integrate AWS Serverless components together
- Manage AWS roles, permissions
- Meetup event APIs require OAuth2.0
- Develop, collaborate and test on cloud instead of local machine

## Accomplishments that we're proud of
- We detailed investigated the AWS Serverless service platforms and applied them to our developments.
- We understood and managed AWS IAS and authentications of API-Gateway and DynamoDB. 
- By using the AWS services we accelerated our development without considering the deployment of our codes on servers.
- We developed a full-rounded API with oauth2, which ensured the security of our API's access.
- //We applied Lambda, API-Gateway and DynamoDB to complete our work.

## What we learned
- We learned how to apply Lambda, API-Gateway and DynamoDB to our developments.
- We learned how oauth2 works in web services.
- We learned how to manage IAS roles management.// and develop with AWS.
- We learned how to use Cloud 9 IDE to develop, collaborate and test Lambda functions.

## What's next for api-world-neu-boss-serverless-api

We plan to create a beautiful web-page and a mobile application for later use. In these application, we wanna to use AWS Route 53 to manage our domain and use API gateway for user authentication. After that, we want to collect some user data to train a machine learning model and create a recommend-algorithm. We think that could make our application more useful and powerful. 
