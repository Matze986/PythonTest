pipeline {
  agent any
  parameters {
        string(name: 'PackageMetadata', description: 'Metadata of the package as JSON')
        string(name: 'PackageContentS3Key', description: 'Key in the S3 bucket with the content of the package as a zip file')
        string(name: 'Email', description: 'Email address of the user that uploaded the package')
        string(name: 'BaseUrl', description: 'Given BaseURL from InFoSim instance')
    }
  stages {
    stage('version') {
      steps {
        sh 'python3 --version'
      }
    }
    stage('hello') {
      steps {
        echo "Hi, execute it!"
        sh 'python3 hello.py "[1, 2, 3, 4, 5]"'
      }
    }
  }
}