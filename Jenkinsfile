def project = "conan-flatbuffers"
def centos = docker.image('essdmscdm/centos-build-node:0.2.5')
def container_name = "${project}-${env.BRANCH_NAME}-${env.BUILD_NUMBER}"

node('docker') {
    def run_args = "\
       --name ${container_name} \
       --tty \
       --network=host \
       --env http_proxy=${env.http_proxy} \
       --env https_proxy=${env.https_proxy} \
       --env local_conan_server=${env.local_conan_server}"

   try {
        container = centos.run(run_args)

        stage('Checkout') {
            def checkout_script = """
                git clone https://github.com/ess-dmsc/${project}.git \
                    --branch ${env.BRANCH_NAME}
            """
            sh "docker exec ${container_name} sh -c \"${checkout_script}\""
        }

        stage('Conan setup') {
            withCredentials(
                    [usernamePassword(
                        credentialsId: 'conan-server-local',
                        passwordVariable: 'CONAN_PASSWORD',
                        usernameVariable: 'CONAN_USERNAME')
                    ])
            {
                def setup_script = """
                    set +x
                    export http_proxy=''
                    export https_proxy=''
                    conan remote add \
                        --insert 0 \
                        ess-dmsc-local ${local_conan_server}
                    conan user \
                        --password '${CONAN_PASSWORD}' \
                        --remote ess-dmsc-local \
                        '${CONAN_USERNAME}'
                """
                sh "docker exec ${container_name} sh -c \"${setup_script}\""
            }
        }

        stage('Package') {
            def package_script = """
                cd ${project}
                conan create ess-dmsc/testing
            """
            sh "docker exec ${container_name} sh -c \"${package_script}\""
        }

        stage('Upload') {
            def package_script = """
                export http_proxy=''
                https_proxy=''
                cd ${project}
                conan upload \
                    --all \
                    --remote ess-dmsc-local \
                    FlatBuffers/1.5.0@ess-dmsc/testing
            """
            sh "docker exec ${container_name} sh -c \"${package_script}\""
        }
    } finally {
        container.stop()
    }
}
