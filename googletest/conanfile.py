from conans import ConanFile, CMake, tools


class CryptoPPConan(ConanFile):
    name = 'googletest'
    version = '1.8.0'
    url = 'https://github.com/wsbu/conan-packages'
    description = "Google's C++ test framework."
    settings = 'os', 'compiler', 'build_type', 'arch'
    license = 'BSD 3-clause "New" or "Revised" License'
    options = {'shared': [True, False]}
    default_options = 'shared=True'
    generators = 'cmake'

    def source(self):
        self.run('git clone --depth=1 https://github.com/google/googletest.git -b release-1.8.0')

        # Without this, CMake won't know how to find the dependencies that Conan is trying to inject
        # Also, set the `conan_output_dirs_setup()` macro to empty or else unit tests will fail
        tools.replace_in_file('googletest/CMakeLists.txt', 'project( googletest-distribution )',
                              '''project( googletest-distribution )
include("${PROJECT_BINARY_DIR}/conanbuildinfo.cmake")
macro(conan_output_dirs_setup)
endmacro()
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)

        cmake.configure(source_dir='googletest', defs={
            'gtest_build_tests': 'TRUE',
            'gmock_build_tests': 'TRUE'
        })
        cmake.build()
        cmake.install()

        # Exclusion due to https://github.com/google/googletest/issues/845
        self.run('ctest --output-on-failure --exclude-regex gtest_catch_exceptions_test', cwd=self.build_folder)

    def package_info(self):
        self.cpp_info.libs = [
            'gtest',
            'gtest_main',
            'gmock',
            'gmock_main'
        ]
