from conans import ConanFile, CMake


class CryptoPPConan(ConanFile):
    name = 'googletest'
    version = '1.8.0'
    url = 'https://github.com/google/googletest'
    description = "Google's C++ test framework."
    settings = 'os', 'compiler', 'build_type', 'arch'
    license = 'BSD 3-clause "New" or "Revised" License'
    options = {'shared': [True, False]}
    default_options = 'shared=True'

    def source(self):
        self.run('git clone --depth=1 https://github.com/google/googletest.git -b release-1.8.0')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_dir='googletest')
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = [
            'gtest',
            'gtest_main',
            'gmock',
            'gmock_main'
        ]
