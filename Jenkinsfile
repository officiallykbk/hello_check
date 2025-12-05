pipeline {
    agent any
    
    environment {
        // REPLACE THESE WITH YOUR ACTUAL VALUES
        AWS_ACCOUNT_ID = "956152914193" 
        AWS_REGION     = "eu-north-1"
        ECR_REPO_NAME  = "test1"
        APP_SERVER_IP  = "13.60.54.137" 
        
        // Calculated variables
        ECR_REGISTRY = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
        IMAGE_URI    = "${ECR_REGISTRY}/${ECR_REPO_NAME}:${env.BUILD_NUMBER}"
    }

    stages {
        stage('Build & Push Image') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-ecr-creds'
                ]]) {
                    script {
                        echo "--- Debug: Checking AWS Identity ---"
                        // This checks if Jenkins is using the correct credentials (User 956152914193)
                        bat "aws sts get-caller-identity"

                        echo "--- 1. Logging into AWS ECR ---"
                        // 'bat' handles the pipe (|) much better than PowerShell on Windows
                        bat "aws ecr get-login-password --region %AWS_REGION% | docker login --username AWS --password-stdin %ECR_REGISTRY%"

                        echo "--- 2. Building Docker Image ---"
                        bat "docker build -t %IMAGE_URI% ."

                        echo "--- 3. Pushing to ECR ---"
                        bat "docker push %IMAGE_URI%"
                    }
                }
            }
        }

      stage('Deploy to App Server') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'JenkinsApp', keyFileVariable: 'MY_KEY_FILE', usernameVariable: 'MY_SSH_USER')]) {
                    script {
                        echo "--- 4. Connecting to App Server ---"
                        
                        // FIX: We MUST fix the file permissions or SSH will ignore the key.
                        // This command removes 'inherited' rights and gives ONLY the current user Full Control (:F).
                        bat 'icacls "%MY_KEY_FILE%" /inheritance:r /grant "%USERNAME%":F'
                        
                        // Define the remote command
                        def remoteCmd = "aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY} && docker pull ${IMAGE_URI} && docker stop devdeploy_app || true && docker rm devdeploy_app || true && docker run -d --name devdeploy_app -p 8000:8000 ${IMAGE_URI}"
                        
                        // Run SSH
                        bat "ssh -o StrictHostKeyChecking=no -i %MY_KEY_FILE% ubuntu@%APP_SERVER_IP% \"${remoteCmd}\""
                    }
                }
            }
        }
    }
}