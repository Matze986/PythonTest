pipeline {
  agent any
  parameters {
    string(name: 'PackageMetadata', description: 'Metadata of the package as JSON')
  }
  stages {
    stage('hello') {
      steps {
        echo "Executing hello.py script"
        sh "python3 hello.py '${PackageMetadata.replaceAll('\'', '\\\\\'')}'"
      }
    }
  }
}
