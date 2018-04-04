pipeline {
  agent {
    node {
      label 'openmeta'
    }
    
  }
  stages {
    stage('Run OpenMETA') {
      steps {
        openMetaTestBench(maxConfigs: '2', modelName: 'openmeta-rocket.xme')
      }
    }
  }
}