import argparse
from http.client import responses

import boto3
from boto3 import client
from botocore.exceptions import ClientError

# Function to delete code deployment group
def delete_codedeploy_deployment_group(application_name, deployment_group_name):
    client = boto3.client('codedeploy')

    try:
        response = client.delete_deployment_group(
            applicationName=application_name,
            deploymentGroupName=deployment_group_name
        )
        print(f"Deployment group '{deployment_group_name}' in application '{application_name}' deleted successfully.")
        return response

    except ClientError as e:
        print(f"Error occurred while deleting deployment group: {e}")
        return None

# Example usage
# delete_codedeploy_deployment_group('MyApplication', 'MyDeploymentGroup')

# Function to delete codedeploy application
def delete_codedeploy_application(application_name):
    # Create a CodeDeploy client
    client = boto3.client('codedeploy')

    try:
        # Delete the CodeDeploy application
        response = client.delete_application(
            applicationName=application_name
        )
        print(f"Application '{application_name}' deleted successfully.")
        return response

    except ClientError as e:
        print(f"Error occurred while deleting the application '{application_name}': {e}")
        return None

# Function to delete sns subscription
def unsubscribe_sns(subscription_arn):
    # Create an SNS client
    sns_client = boto3.client('sns')

    try:
        # Call the unsubscribe API
        response = sns_client.unsubscribe(
            SubscriptionArn=subscription_arn
        )
        print(f"Subscription '{subscription_arn}' has been successfully unsubscribed.")
        return response

    except ClientError as e:
        print(f"Error occurred while unsubscribing: {e}")
        return None

# Function to delete cloudwatch alarms
def delete_cloudwatch_alarm(alarm_name):
    client = boto3.client('cloudwatch')

    try:
        response = client.delete_alarms(
            AlarmNames=[alarm_name]
        )
        print(f"CloudWatch alarm '{alarm_name}' deleted successfully.")
        return response

    except ClientError as e:
        print(f"Error occurred while deleting alarm: {e}")
        return None

# Function to delete sns topics
def delete_sns_topic(topic_arn):
    client = boto3.client('sns')
    try:
        response = client.delete_topic(TopicArn=topic_arn)
        print(f"Topic '{topic_arn}' deleted successfully.")
        return response
    except ClientError as e:
        print(f"An error occurred: {e}")
        return None

# Function to delete Lambdas
def delete_lambda(function_arn):
    lambda_client = boto3.client ('lambda')
    try:
        response = lambda_client.delete_function(FunctionName=function_arn)
        print(f"Lambda '{function_arn}' deleted successfully")
        return response
    except ClientError as e:
        print(f"An error occurred; {e}")
        return None

def main():
    # Main parser
    parser = argparse.ArgumentParser(description='AWS Resource Deletion Management')
    subparsers = parser.add_subparsers(dest='command')

    # Subparser for deleting a deployment group
    delete_group_parser = subparsers.add_parser('delete_deployment_group', help='Delete a CodeDeploy deployment group')
    delete_group_parser.add_argument('application_name', help='Name of the CodeDeploy application')
    delete_group_parser.add_argument('deployment_group_name', help='Name of the deployment group')

    # Subparser for deleting an application
    delete_app_parser = subparsers.add_parser('delete_application', help='Delete a CodeDeploy application')
    delete_app_parser.add_argument('application_name', help='Name of the CodeDeploy application')

    # Subparser for deleting subscriptions
    unsubscribe_sns_parser = subparsers.add_parser('unsubscribe_sns', help='Delete SNS subscriptions')
    unsubscribe_sns_parser.add_argument('subscription_arn', help='ARN of the sns subscription')

    # Subparser for deleting cloudwatch
    delete_alarm_parser= subparsers.add_parser('delete_cloudwatch_alarm', help='Delete cloudwatch alarm')
    delete_alarm_parser.add_argument('alarm_name', help='Alarm name')

    # Subparser for deleting SNS topics
    delete_sns_topic_parser = subparsers.add_parser('delete_sns_topic', help='Delete SNS topic')
    delete_sns_topic_parser.add_argument('topic_arn', help='SNS topic subscription')

    #Subparser for deleting Lambda function
    delete_lambda_parser = subparsers.add_parser('delete_lambda', help='Delete Lambda Functions')
    delete_lambda_parser.add_argument('function_arn', help='Lambda function')

    args = parser.parse_args()

    if args.command == 'delete_deployment_group':
        delete_codedeploy_deployment_group(args.application_name, args.deployment_group_name)
    elif args.command == 'delete_application':
        delete_codedeploy_application(args.application_name)
    elif args.command == 'unsubscribe_sns':
        unsubscribe_sns(args.subscription_arn)
    elif args.command == 'delete_cloudwatch_alarm':
        delete_cloudwatch_alarm(args.alarm_name)
    elif args.command =='delete_sns_topic':
        delete_sns_topic(args.topic_arn)
    elif args.command == 'delete_lambda':
        delete_lambda(args.function_arn)
    else:
        print("No valid command provided. Use 'delete_deployment_group', 'delete_application', 'unsubscribe_sns', 'delete_cloudwatch_alarm', 'delete_sns_topic', or 'delete_lambda'.")

if __name__ == '__main__':
    main()