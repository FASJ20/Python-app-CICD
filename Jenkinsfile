pipeline {
    agent any

    environment {
        // Customize these variables
        DOCKER_IMAGE = "fasj/python-container-app"
        KUBE_CONFIG = "--kubeconfig=$HOME\.kube\config"  // Only needed if Jenkins isn't in-cluster
    }

    stages {
        // Stage 1: Checkout Code
        stage('Checkout Git') {
            steps {
                git branch: 'main', 
                url: 'https://github.com/FASJ20/Python-app-CICD.git'
            }
        }

        // Stage 2: Build Docker Image
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${env.BUILD_ID}")
                }
            }
        }

        // Stage 3: Push to Docker Hub (or ECR)
        stage('Push to Registry') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-creds') {
                        docker.image("${DOCKER_IMAGE}:${env.BUILD_ID}").push()
                    }
                }
            }
        }

        // Stage 4: Deploy to Kubernetes
        stage('Deploy to K8s') {
            steps {
                // Update deployment.yaml with new image
                sh """
                    sed -i 's|image: .*|image: ${DOCKER_IMAGE}:${env.BUILD_ID}|' k8s/deployment.yaml
                    kubectl ${KUBE_CONFIG} apply -f k8s/
                """
            }
        }

        // Stage 5: Verify Deployment (Optional)
        stage('Smoke Test') {
            steps {
                script {
                    def rolloutStatus = sh(
                        script: "kubectl ${KUBE_CONFIG} rollout status deployment/myapp-deployment --timeout=30s",
                        returnStatus: true
                    )
                    if (rolloutStatus != 0) {
                        error("Deployment failed!")
                    }
                }
            }
        }
    }

    post {
        failure {
            slackSend channel: '#devops-alerts',
                     message: "Build ${env.BUILD_ID} failed! See ${env.BUILD_URL}"
        }
        success {
            echo "Deployed ${DOCKER_IMAGE}:${env.BUILD_ID} successfully!"
        }
    }
}