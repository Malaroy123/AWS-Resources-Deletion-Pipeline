pipeline {
    agent {
        docker {
            image 'python:3.9-slim'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    parameters {
        choice(name: 'COMMAND', choices: [
            'delete_deployment_group',
            'delete_application',
            'unsubscribe_sns',
            'delete_cloudwatch_alarm', 
            'delete_sns_topic',
            'delete_lambda'
        ], description: 'Select the resource you want to delete')

        string(name: 'AWS_ACCOUNT', defaultValue: '', description: 'AWS Account Number')
        string(name: 'AWS_REGION', choices: ['eu-west-1', 'eu-west-2'], description: 'Select the AWS Region')
        string(name: 'APPLICATION_NAME', defaultValue: '', description: 'CodeDeploy application name (if applicable)')
        string(name: 'DEPLOYMENT_GROUP_NAME', defaultValue: '', description: 'Deployment group name (if applicable)')
        string(name: 'SUBSCRIPTION_NAME', defaultValue: '', description: 'SNS subscription ARN (if applicable)')
        string(name: 'ALARM_NAME', defaultValue: '', description: 'CloudWatch alarm name (if applicable)')
        string(name: 'TOPIC_ARN', defaultValue: '', description: 'SNS topic ARN (if applicable)')
        string(name: 'FUNCTION_ARN', defaultValue: '', description: 'Lambda function ARN (if applicable)')
    }
    
    environment {
        AWS_ACCOUNT = params.AWS_ACCOUNT
        AWS_REGION = params.AWS_REGION
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run AWS Resource Deletion') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-credentials'
                ]]) {
                    script {
                        def cmd = ""
                        switch (params.COMMAND) {
                            case 'delete_deployment_group':
                                if (!params.APPLICATION_NAME?.trim() || !params.DEPLOYMENT_GROUP_NAME?.trim()) {
                                    error "APPLICATION_NAME and DEPLOYMENT_GROUP_NAME are required for delete_deployment_group"
                                }
                                cmd = "python3 deletion_script.py delete_deployment_group ${params.APPLICATION_NAME} ${params.DEPLOYMENT_GROUP_NAME}"
                                break
                            case 'delete_application':
                                if (!params.APPLICATION_NAME?.trim()) {
                                    error "APPLICATION_NAME is required for delete_application"
                                }
                                cmd = "python3 deletion_script.py delete_application ${params.APPLICATION_NAME}"
                                break
                            case 'unsubscribe_sns':
                                if (!params.SUBSCRIPTION_NAME?.trim()) {
                                    error "SUBSCRIPTION_NAME is required for unsubscribe_sns"
                                }
                                cmd = "python3 deletion_script.py unsubscribe_sns ${params.SUBSCRIPTION_NAME}"
                                break
                            case 'delete_cloudwatch_alarm':
                                if (!params.ALARM_NAME?.trim()) {
                                    error "ALARM_NAME is required for delete_cloudwatch_alarm"
                                }
                                cmd = "python3 deletion_script.py delete_cloudwatch_alarm ${params.ALARM_NAME}"
                                break
                            case 'delete_sns_topic':
                                if (!params.TOPIC_ARN?.trim()) {
                                    error "TOPIC_ARN is required for delete_sns_topic"
                                }
                                cmd = "python3 deletion_script.py delete_sns_topic ${params.TOPIC_ARN}"
                                break
                            case 'delete_lambda':
                                if (!params.FUNCTION_ARN?.trim()) {
                                    error "FUNCTION_ARN is required for delete_lambda"
                                }
                                cmd = "python3 deletion_script.py delete_lambda ${params.FUNCTION_ARN}"
                                break
                            default:
                                error "Invalid command: ${params.COMMAND}"
                        }

                        echo "Using AWS Account: ${env.AWS_ACCOUNT} and Region: ${env.AWS_REGION}"
                        echo "Executing command: ${cmd}"

                        sh "${cmd}"
                    }
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline completed with result: ${currentBuild.result}"
        }
    }
}