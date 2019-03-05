from conans.model.conan_file import ConanFile
from conans import CMake
import os


class TinyXMLTestConan(ConanFile):
    settings = "os", "compiler", "arch", "build_type", "platform"
    generators = "cmake_find_package"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        CMake(self).test()
        assert os.path.exists(os.path.join(self.deps_cpp_info["tinyxml"].rootpath, 'etc', 'license', 'tinyxml'))
