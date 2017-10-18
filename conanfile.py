import os
from conans import ConanFile, CMake, tools
from conans.util import files


class FlatbuffersConan(ConanFile):
    name = "FlatBuffers"
    version = "1.5.0"
    license = "BSD 2-Clause"
    url = "https://github.com/ess-dmsc/conan-flatbuffers"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    options = {"shared": [True, False]}
    default_options = "shared=False"

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
        files.mkdir("./flatbuffers-1.5.0/build")
        with tools.chdir("./flatbuffers-1.5.0/build"):
            cmake = CMake(self)

            cmake.definitions["FLATBUFFERS_BUILD_TESTS"] = "OFF"
            cmake.definitions["FLATBUFFERS_INSTALL"] = "OFF"
            if self.options.shared:
                cmake.definitions["FLATBUFFERS_BUILD_FLATLIB"] = "OFF"
                cmake.definitions["FLATBUFFERS_BUILD_SHAREDLIB"] = "ON"
            else:
                cmake.definitions["FLATBUFFERS_BUILD_FLATLIB"] = "ON"
                cmake.definitions["FLATBUFFERS_BUILD_SHAREDLIB"] = "OFF"

            cmake.configure(source_dir="..", build_dir=".")
            cmake.build(build_dir=".")

    def package(self):
        with tools.chdir("flatbuffers-1.5.0"):
            self.copy("flatc", dst="bin",
                      src="flatbuffers-1.5.0/build", keep_path=False)
            self.copy("flathash", dst="bin",
                      src="flatbuffers-1.5.0/build", keep_path=False)
            self.copy("*.h", dst="include/flatbuffers",
                      src="flatbuffers-1.5.0/include/flatbuffers")
            self.copy("*.a", dst="lib",
                      src="flatbuffers-1.5.0/build", keep_path=False)
            self.copy("*.so", dst="lib",
                      src="flatbuffers-1.5.0/build", keep_path=False)
            self.copy("*.dylib", dst="lib",
                      src="flatbuffers-1.5.0/build", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["flatbuffers"]
