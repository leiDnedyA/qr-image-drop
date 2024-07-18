pipeline {
  agent any
  stages {
    stage('Setup') {
      steps {
        sh "python3 -m venv venv"
        sh '''#!/bin/bash
              source venv/bin/activate
              pip3 install -r requirements.txt
        '''
      }
    }
    stage('Run') {
      steps {
        sh '''#!/bin/bash
              source venv/bin/activate
              nohup gunicorn -b 0.0.0.0:3000 app:app &
        '''
        echo 'Running ${env.BUILD_ID} on ${env.JENKINS_URL}...'
        sh 'pwd'
        echo 'Finished :)'
      }
    }
  }
}

