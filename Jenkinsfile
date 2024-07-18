pipeline {
  agent any
  stages {
    stage('Setup') {
      steps {
        sh "python3 -m venv venv"
        sh "source venv/bin/activate"
        sh "pip3 install -r requirements.txt"
      }
    }
    stage('Run') {
      steps {
        echo 'Running ${env.BUILD_ID} on ${env.JENKINS_URL}...'
        sleep 20
        echo 'Finished :)'
      }
    }
  }
}

