import argparse
from http.client import responses
import boto3
from boto3 import client
from botocore.exceptions import ClientError

def delete_deployment_group(application_name, deployment_group_name, region):
    client = boto3.client('codedeploy', region_name=region)
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
    try:
        client.delete_application(
            applicationName=application_name
        )
        print(f"Successfully deleted application: {application_name}")
    except ClientError as e:
        print(f"Error deleting application: {e}")
        raise

def unsubscribe_sns(subscription_arn, region):
    client = boto3.client('sns', region_name=region)
    try:
        client.unsubscribe(
            SubscriptionArn=subscription_arn
        )
        print(f"Successfully unsubscribed from SNS topic: {subscription_arn}")
    except ClientError as e:
        print(f"Error unsubscribing from SNS topic: {e}")
        raise

def delete_cloudwatch_alarm(alarm_name, region):
    client = boto3.client('cloudwatch', region_name=region)
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
    try:
        client.delete_function(
            FunctionName=function_arn
        )
        print(f"Successfully deleted Lambda function: {function_arn}")
    except ClientError as e:
        print(f"Error deleting Lambda function: {e}")
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
    parser.add_argument('application_name', nargs='?', help='Application name (for delete_deployment_group, delete_application, delete_cloudwatch_alarm)')
    parser.add_argument('deployment_group_name', nargs='?', help='Deployment group name (for delete_deployment_group)')
    parser.add_argument('resource_arn', nargs='?', help='Resource ARN (for unsubscribe_sns, delete_sns_topic, delete_lambda)')
    parser.add_argument('--region', required=True, help='AWS region')
    
    args = parser.parse_args()

    try:
        if args.command == 'delete_deployment_group':
            if not args.application_name or not args.deployment_group_name:
                raise ValueError("Both application name and deployment group name are required for delete_deployment_group")
            delete_deployment_group(args.application_name, args.deployment_group_name, args.region)
        
        elif args.command == 'delete_application':
            if not args.application_name:
                raise ValueError("Application name is required for delete_application")
            delete_application(args.application_name, args.region)
        
        elif args.command == 'delete_cloudwatch_alarm':
            if not args.application_name:
                raise ValueError("Application name is required for delete_cloudwatch_alarm")
            delete_cloudwatch_alarm(args.application_name, args.region)
        
        elif args.command in ['unsubscribe_sns', 'delete_sns_topic', 'delete_lambda']:
            if not args.resource_arn:
                raise ValueError(f"Resource ARN is required for {args.command}")
            if args.command == 'unsubscribe_sns':
                unsubscribe_sns(args.resource_arn, args.region)
            elif args.command == 'delete_sns_topic':
                delete_sns_topic(args.resource_arn, args.region)
            else:
                delete_lambda(args.resource_arn, args.region)

    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == '__main__':
    main()