import os

from conans import CMake, ConanFile


class ZeroMQTest(ConanFile):
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake"

    def build(self):
        cmake = self.cmake
        cmake.configure()
        cmake.build()

    def test(self):
        self.cmake.test()

    @property
    def cmake(self):
        cmake = CMake(self)
        return cmake
