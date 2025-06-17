pipeline {
    agent any
    triggers {
        githubPush()
    }
    stages {
        stage('Clone source') {
            steps {
                git url: 'https://github.com/NoTPr0/aqa_070225', branch: 'homework_30'
            }
        }
        stage('Build and activate venv') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        stage('Tests') {
            steps {
                sh '''
                . venv/bin/activate
                pytest -s -v "$WORKSPACE/lesson_24/test_lesson_24.py" --junitxml=$WORKSPACE/report.xml
                '''
                junit '**/report.xml'
            }
        }
    }
    post {
        always {
            emailext (
                subject: "Результати тестування Jenkins: ${currentBuild.fullDisplayName}",
                body: """<p>Білд завершено з результатом: ${currentBuild.currentResult}</p>
                         <p>Перевір звіт у вкладці 'Test Results' або на Jenkins:</p>
                         <p><a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>""",
                to: 'vadymhello.work@gmail.com',
                from: 'vadymhello.work@gmail.com',
                attachmentsPattern: '**/report.html',
                mimeType: 'text/html'
            )
        }
    }
}
