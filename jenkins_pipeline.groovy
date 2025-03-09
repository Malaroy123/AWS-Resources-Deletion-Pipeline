pipeline {
    agent any

    parameters {
        choice(name: 'COMMAND', choices: [
            'delete_deployment_group',
            'delete_application',
            'unsubscribe_sns',
            'delete_cloudwatch_alarm', 
            'delete_sns_topic',
            'delete_lambda'
        ], description: 'Select the resource to delete')

        string(name: 'AWS_ACCOUNT', defaultValue: '', description: 'AWS Account Number')
        choice(name: 'AWS_REGION', choices: ['eu-west-1', 'eu-west-2'], description: 'Select the AWS Region')
        string(name: 'APPLICATION_NAME', defaultValue: '', description: 'Application name (required for delete_deployment_group, delete_application, Cloudwatch Alarms)')
        string(name: 'DEPLOYMENT_GROUP_NAME', defaultValue: '', description: 'Deployment group name (required for delete_deployment_group)')
        string(name: 'RESOURCE_ARN', defaultValue: '', description: 'Resource ARN (required for SNS subscriptions/topics, Lambda operations)')
    }
    
    environment {
        AWS_ACCOUNT = "${params.AWS_ACCOUNT}"
        AWS_REGION = "${params.AWS_REGION}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Setup Python') {
            steps {
                sh '''
                    #!/bin/bash
                    # Create virtual environment
                    python3 -m venv venv
                    
                    # Activate virtual environment
                    source venv/bin/activate
                    
                    # Install requirements
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Validate Parameters') {
            steps {
                script {
                    echo "Validating input parameters..."
                    switch(params.COMMAND) {
                        case 'delete_deployment_group':
                            if (!params.APPLICATION_NAME?.trim() || !params.DEPLOYMENT_GROUP_NAME?.trim()) {
                                error "APPLICATION_NAME and DEPLOYMENT_GROUP_NAME are required for delete_deployment_group"
                            }
                            break
                        case 'delete_application':
                        case 'delete_cloudwatch_alarm':
                            if (!params.APPLICATION_NAME?.trim()) {
                                error "APPLICATION_NAME is required for ${params.COMMAND}"
                            }
                            break
                        case 'unsubscribe_sns':
                        case 'delete_sns_topic':
                        case 'delete_lambda':
                            if (!params.RESOURCE_ARN?.trim()) {
                                error "RESOURCE_ARN is required for ${params.COMMAND}"
                            }
                            break
                        default:
                            error "Invalid command: ${params.COMMAND}"
                    }
                    echo "Parameter validation successful"
                }
            }
        }

        stage('Delete AWS Resource') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-credentials'
                ]]) {
                    script {
                        def cmd = ""
                        switch(params.COMMAND) {
                            case 'delete_deployment_group':
                                cmd = "python3 deletion_script.py ${params.COMMAND} ${params.APPLICATION_NAME} ${params.DEPLOYMENT_GROUP_NAME} --region ${params.AWS_REGION}"
                                break
                            case 'delete_application':
                            case 'delete_cloudwatch_alarm':
                                cmd = "python3 deletion_script.py ${params.COMMAND} ${params.APPLICATION_NAME} --region ${params.AWS_REGION}"
                                break
                            case 'unsubscribe_sns':
                            case 'delete_sns_topic':
                            case 'delete_lambda':
                                cmd = "python3 deletion_script.py ${params.COMMAND} ${params.RESOURCE_ARN} --region ${params.AWS_REGION}"
                                break
                        }

                        echo "Using AWS Account: ${env.AWS_ACCOUNT} and Region: ${env.AWS_REGION}"
                        echo "Executing command: ${cmd}"

                        sh """
                            #!/bin/bash
                            set -e  # Exit immediately if a command exits with a non-zero status
                            source venv/bin/activate
                            export AWS_DEFAULT_REGION=${params.AWS_REGION}
                            ${cmd}
                        """
                    }
                }
            }
        }
    }

    post {
        success {
            echo "Successfully deleted AWS resource"
        }
        failure {
            echo "Failed to delete AWS resource"
        }
        always {
            echo "Pipeline completed with result: ${currentBuild.result}"
        }
    }
}