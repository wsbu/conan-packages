from conans.model.conan_file import ConanFile
from conans import CMake
import os
import sys


class DefaultNameConan(ConanFile):
    name = "DefaultName"
    version = "0.1"
    settings = "os", "compiler", "arch", "build_type"
    options = {'shared': [True, False]}
    default_options = 'shared=False'
    generators = "cmake"

    def configure(self):
        if self.options["Boost"].header_only:
            self.settings.clear()

    def build(self):
        cmake = CMake(self)
        if self.options["Boost"].header_only:
            cmake.definitions["HEADER_ONLY"] = "TRUE"
        if self.options["Boost"].python:
            cmake.definitions["WITH_PYTHON"] = "TRUE"
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy(pattern="*.dll", dst="bin", src="bin")
        self.copy(pattern="*.dylib", dst="bin", src="lib")

    def test(self):
        self.run('ctest --output-on-error')
        if self.options["Boost"].python:
            os.chdir("bin")
            sys.path.append(".")
            import hello_ext
            hello_ext.greet()
