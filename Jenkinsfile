pipeline {
  agent any
  environment {
    REGISTRY    = "docker.io"
    DOCKER_USER = "zk0061"         // your Docker Hub username
    IMAGE_NAME  = "demo-web"
    TAG         = "${env.BUILD_NUMBER}"
  }
  options { timestamps() }

  stages {
    stage('Checkout') { steps { checkout scm } }

    stage('Build Docker image') {
      steps {
        sh '''
          set -eux
          docker build -t $REGISTRY/$DOCKER_USER/$IMAGE_NAME:$TAG .
          docker tag   $REGISTRY/$DOCKER_USER/$IMAGE_NAME:$TAG $REGISTRY/$DOCKER_USER/$IMAGE_NAME:latest
        '''
      }
    }

    stage('Push to Docker Hub') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DU', passwordVariable: 'DP')]) {
          sh '''
            set -eux
            echo "$DP" | docker login -u "$DU" --password-stdin $REGISTRY
            docker push $REGISTRY/$DOCKER_USER/$IMAGE_NAME:$TAG
            docker push $REGISTRY/$DOCKER_USER/$IMAGE_NAME:latest
          '''
        }
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        withCredentials([file(credentialsId: 'kubeconfig', variable: 'KCF')]) {
          sh '''
            set -eux
            export KUBECONFIG="$KCF"
            sed "s/{{TAG}}/$TAG/g; s/DOCKER_USER/$DOCKER_USER/g" k8s/deployment.yaml > k8s/deployment.rendered.yaml
            minikube kubectl -- apply -f k8s/deployment.rendered.yaml
            minikube kubectl -- apply -f k8s/service.yaml
            minikube kubectl -- rollout status deploy/demo-web --timeout=120s
          '''
        }
      }
    }
  }

  post {
    success { echo "✅ Deployed $REGISTRY/$DOCKER_USER/$IMAGE_NAME:$TAG" }
    failure { echo "❌ Build failed — open Console Output for details." }
  }
}
