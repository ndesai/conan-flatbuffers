import os
from conans import ConanFile, CMake, tools


class FlatbuffersConan(ConanFile):
    name = "FlatBuffers"
    version = "1.5.0"
    license = "BSD 2-Clause"
    url = "https://github.com/ess-dmsc/conan-flatbuffers"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def source(self):
        tools.download(
            "https://github.com/google/flatbuffers/archive/v1.5.0.tar.gz",
            "flatbuffers-1.5.0.tar.gz"
        )
        tools.check_sha256(
            "flatbuffers-1.5.0.tar.gz",
            "85362cb54042e96329cb65396a5b589789b3d42e4ed7c2debddb7a2300a05f41"
        )
        tools.unzip("flatbuffers-1.5.0.tar.gz")
        os.unlink("flatbuffers-1.5.0.tar.gz")

    def build(self):
        cmake = CMake(self)
        self.run('cmake flatbuffers-1.5.0 %s' % cmake.command_line)
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("flatc", dst="bin", keep_path=False)
        self.copy("*.h", dst="include/flatbuffers",
                  src="flatbuffers-1.5.0/include/flatbuffers")
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["flatbuffers"]
