pipeline {
  agent any
  stages {
    stage('version') {
      steps {
        sh 'python3 --version'
      }
    }
    stage('hello') {
      steps {
        echo "Hi, execute it!"
        sh 'python3 hello.py'
      }
    }
  }
}