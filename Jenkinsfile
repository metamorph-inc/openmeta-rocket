pipeline {
  agent any
  stages {
    stage('Run OpenMETA') {
      steps {
        openMetaTestBench(maxConfigs: '2', modelName: 'openmeta-rocket.xme')
      }
    }
  }
}