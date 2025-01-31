pipeline {
  agent any
  parameters {
    string(name: 'PackageMetadata', description: 'Metadata of the package as JSON')
    string(name: 'PackageContentS3Key', description: 'Metadata of the package as JSON')
    string(name: 'Email', description: 'Metadata of the package as JSON')
    string(name: 'BaseUrl', description: 'Metadata of the package as JSON')
  }
  stages {
    stage('hello') {
      steps {
        echo "Executing hello.py script"
        sh "python3 hello.py '${PackageMetadata}' '${PackageContentS3Key}' '${Email}' '${BaseUrl}'"
      }
    }
  }
}
