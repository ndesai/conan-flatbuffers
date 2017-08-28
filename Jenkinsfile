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
       --mount type=bind,readonly=true,src=/home/jenkins/.conan/cacert.pem,dst=/conan/.conan/cacert.pem \
       --mount type=bind,readonly=true,src=/home/jenkins/.conan/.conan.db,dst=/conan/.conan/.conan.db"

   try {
        container = centos.run(run_args)

        stage('Checkout') {
            def checkout_script = """
                git clone https://github.com/ess-dmsc/${project}.git \
                    --branch ${env.BRANCH_NAME}
            """
            sh "docker exec ${container_name} sh -c \"${checkout_script}\""
        }

        stage('Package') {
            // Copy Conan registry containing ess-dmsc-local Conan server.
            sh "docker cp /home/jenkins/.conan/registry.txt ${container_name}:/conan/.conan/registry.txt"
            def package_script = """
                cd ${project}
                conan create ess-dmsc/testing
                http_proxy="" https_proxy="" conan upload --remote ess-dmsc-local FlatBuffers/1.5.0@ess-dmsc/testing --all
            """
            sh "docker exec ${container_name} sh -c \"${package_script}\""
        }
    } finally {
        container.stop()
    }
}
