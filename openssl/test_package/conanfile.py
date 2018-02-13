from conans.model.conan_file import ConanFile
from conans import CMake
import os


class OpenSSLTestConan(ConanFile):
    settings = "os", "compiler", "arch", "build_type"
    options = {'shared': [True, False]}
    default_options = 'shared=False'
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        self.run('ctest --output-on-failure')
        assert os.path.exists(os.path.join(self.deps_cpp_info["OpenSSL"].rootpath, "LICENSE"))
