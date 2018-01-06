import os
import subprocess

from conans import ConanFile, CMake


class TestBisonConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        test_exe = os.path.join(self.build_folder, 'bin', 'test-bison')
        self.output.info('Running ' + test_exe)
        p = subprocess.Popen([test_exe], stdin=subprocess.PIPE)
        p.communicate("1 + 2* 3\n".encode())
        assert 0 == p.returncode, 'Test failed with non-zero exit code'
