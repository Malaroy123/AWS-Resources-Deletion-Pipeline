import argparse
from http.client import responses
import boto3
from boto3 import client
from botocore.exceptions import ClientError

# Define custom exception at the top of the file
class ResourceNotFoundError(Exception):
    pass

def check_deployment_group_exists(client, application_name, deployment_group_name):
    try:
        client.get_deployment_group(
            applicationName=application_name,
            deploymentGroupName=deployment_group_name
        )
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'DeploymentGroupDoesNotExistException':
            return False
        raise

def check_application_exists(client, application_name):
    try:
        client.get_application(applicationName=application_name)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'ApplicationDoesNotExistException':
            return False
        raise

def check_alarm_exists(client, alarm_name):
    try:
        response = client.describe_alarms(AlarmNames=[alarm_name])
        return len(response['MetricAlarms']) > 0
    except ClientError:
        return False

def check_sns_subscription_exists(client, subscription_arn):
    try:
        client.get_subscription_attributes(SubscriptionArn=subscription_arn)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'NotFound':
            return False
        raise

def check_sns_topic_exists(client, topic_arn):
    try:
        client.get_topic_attributes(TopicArn=topic_arn)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'NotFound':
            return False
        raise

def check_lambda_exists(client, function_arn):
    try:
        client.get_function(FunctionName=function_arn)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            return False
        raise

def delete_deployment_group(application_name, deployment_group_name, region):
    client = boto3.client('codedeploy', region_name=region)
    if not check_deployment_group_exists(client, application_name, deployment_group_name):
        raise ResourceNotFoundError(f"Deployment group '{deployment_group_name}' does not exist in application '{application_name}'")
    try:
        client.delete_deployment_group(
            applicationName=application_name,
            deploymentGroupName=deployment_group_name
        )
        print(f"Successfully deleted deployment group: {deployment_group_name}")
    except ClientError as e:
        print(f"Error deleting deployment group: {e}")
        raise

def delete_application(application_name, region):
    client = boto3.client('codedeploy', region_name=region)
    if not check_application_exists(client, application_name):
        raise ResourceNotFoundError(f"Application '{application_name}' does not exist")
    try:
        client.delete_application(
            applicationName=application_name
        )
        print(f"Successfully deleted application: {application_name}")
    except ClientError as e:
        print(f"Error deleting application: {e}")
        raise

def delete_cloudwatch_alarm(alarm_name, region):
    client = boto3.client('cloudwatch', region_name=region)
    if not check_alarm_exists(client, alarm_name):
        raise ResourceNotFoundError(f"CloudWatch alarm '{alarm_name}' does not exist")
    try:
        client.delete_alarms(
            AlarmNames=[alarm_name]
        )
        print(f"Successfully deleted CloudWatch alarm: {alarm_name}")
    except ClientError as e:
        print(f"Error deleting CloudWatch alarm: {e}")
        raise

def delete_sns_topic(topic_arn, region):
    client = boto3.client('sns', region_name=region)
    if not check_sns_topic_exists(client, topic_arn):
        raise ResourceNotFoundError(f"SNS topic '{topic_arn}' does not exist")
    try:
        client.delete_topic(
            TopicArn=topic_arn
        )
        print(f"Successfully deleted SNS topic: {topic_arn}")
    except ClientError as e:
        print(f"Error deleting SNS topic: {e}")
        raise

def delete_lambda(function_arn, region):
    client = boto3.client('lambda', region_name=region)
    if not check_lambda_exists(client, function_arn):
        raise ResourceNotFoundError(f"Lambda function '{function_arn}' does not exist")
    try:
        client.delete_function(
            FunctionName=function_arn
        )
        print(f"Successfully deleted Lambda function: {function_arn}")
    except ClientError as e:
        print(f"Error deleting Lambda function: {e}")
        raise

def unsubscribe_sns(subscription_arn, region):
    client = boto3.client('sns', region_name=region)
    if not check_sns_subscription_exists(client, subscription_arn):
        raise ResourceNotFoundError(f"SNS subscription '{subscription_arn}' does not exist")
    try:
        client.unsubscribe(
            SubscriptionArn=subscription_arn
        )
        print(f"Successfully unsubscribed from SNS topic: {subscription_arn}")
    except ClientError as e:
        print(f"Error unsubscribing from SNS topic: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(description='Delete AWS resources')
    parser.add_argument('command', choices=[
        'delete_deployment_group',
        'delete_application',
        'unsubscribe_sns',
        'delete_cloudwatch_alarm',
        'delete_sns_topic',
        'delete_lambda'
    ])
    # First positional argument can be either application_name or resource_arn
    parser.add_argument('identifier', help='Application name or Resource ARN depending on the command')
    # Optional second argument for deployment group
    parser.add_argument('deployment_group_name', nargs='?', help='Deployment group name (for delete_deployment_group)')
    parser.add_argument('--region', required=True, help='AWS region')
    
    args = parser.parse_args()

    try:
        if args.command == 'delete_deployment_group':
            if not args.identifier or not args.deployment_group_name:
                raise ValueError("Both application name and deployment group name are required for delete_deployment_group")
            delete_deployment_group(args.identifier, args.deployment_group_name, args.region)
        
        elif args.command == 'delete_application':
            if not args.identifier:
                raise ValueError("Application name is required for delete_application")
            delete_application(args.identifier, args.region)
        
        elif args.command == 'delete_cloudwatch_alarm':
            if not args.identifier:
                raise ValueError("Application name is required for delete_cloudwatch_alarm")
            delete_cloudwatch_alarm(args.identifier, args.region)
        
        elif args.command in ['unsubscribe_sns', 'delete_sns_topic', 'delete_lambda']:
            if not args.identifier:
                raise ValueError(f"Resource ARN is required for {args.command}")
            if args.command == 'unsubscribe_sns':
                unsubscribe_sns(args.identifier, args.region)
            elif args.command == 'delete_sns_topic':
                delete_sns_topic(args.identifier, args.region)
            else:
                delete_lambda(args.identifier, args.region)

    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == '__main__':
    main()