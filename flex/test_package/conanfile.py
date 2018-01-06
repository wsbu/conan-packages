import os
import subprocess

from conans import ConanFile, CMake


class TestFlexConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        with open(os.path.join(self.conanfile_directory, 'basic_nr.txt'), 'r') as f:
            input_text = f.read()
        test_exe = os.path.join(self.build_folder, 'bin', 'test-flex')
        self.output.info('Running ' + test_exe)
        p = subprocess.Popen([test_exe], stdin=subprocess.PIPE)
        p.communicate(input_text.encode())
        assert 0 == p.returncode, 'Test failed with non-zero exit code'
