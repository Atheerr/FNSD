# Deploying a Flask API


This is the Fullstack Developer Nanodegree Project 4 project repository: Server Deployment, Container, and Testing.

In this project, I compiled and deployed the Flask API in the Kubernetes cluster using Docker, AWS EKS, CodePipeline, and CodeBuild.

API endpoint: http://a5b1c2490a7de47b8ad2573070e23dc7-420165840.us-east-2.elb.amazonaws.com/

The Flask application that will be used for this project consists of a simple API with three endpoints:

GET '/': This is a simple medical test, which shows the 'healthy' answer.
POST '/ auth': This takes an email and password as json arguments and returns JWT based on a custom secret.
GET '/ content': This requires a valid JWT, and returns unencrypted content for that token.


## Project Steps

Completing the project involves several steps:

1. Write a Dockerfile for a simple Flask API
2. Build and test the container locally
3. Create an EKS cluster
4. Store a secret using AWS Parameter Store
5. Create a CodePipeline pipeline triggered by GitHub checkins
6. Create a CodeBuild stage which will build, test, and deploy your code


## Acknowledgement
- Thank you very much udacity

- Thanks to coach Elham

