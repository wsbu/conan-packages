import os
from conans import ConanFile, CMake, tools


class CryptoPPConan(ConanFile):
    name = 'googletest'
    version = '1.8.0+1'
    url = 'https://github.com/wsbu/conan-packages'
    description = "Google's C++ test framework."
    settings = 'os', 'compiler', 'build_type', 'arch'
    license = 'BSD 3-clause "New" or "Revised" License'
    options = {
        'shared': [True, False],
        'run_tests': [True, False]
    }
    default_options = 'shared=True', 'run_tests=False'
    generators = 'cmake'

    def source(self):
        self.run('git clone --depth=1 https://github.com/google/googletest.git -b release-1.8.0')

    def build(self):
        source_dir = os.path.join(self.build_folder, 'googletest')
        build_dir = os.path.join(self.build_folder, 'build')

        # Without this, CMake won't know how to find the dependencies that Conan is trying to inject
        # Also, set the `conan_output_dirs_setup()` macro to empty or else unit tests will fail
        tools.replace_in_file(os.path.join(source_dir, 'CMakeLists.txt'), 'project( googletest-distribution )',
                              '''project( googletest-distribution )
include("{0}/conanbuildinfo.cmake")
macro(conan_output_dirs_setup)
endmacro()
conan_basic_setup()'''.format(self.build_folder))

        cmake = CMake(self)
        cmake.definitions['CMAKE_INSTALL_PREFIX'] = '/'

        if tools.cross_building(self.settings) or not self.options.run_tests:
            extra_definitions = {}
        else:
            extra_definitions = {
                'gtest_build_tests': 'TRUE',
                'gmock_build_tests': 'TRUE'
            }
        cmake.configure(source_dir=source_dir, build_dir=build_dir, defs=extra_definitions)
        cmake.build()
        if not tools.cross_building(self.settings) and self.options.run_tests:
            # Exclusion due to https://github.com/google/googletest/issues/845
            self.run('ctest --output-on-failure --exclude-regex gtest_catch_exceptions_test', cwd=self.build_folder)

    def package(self):
        build_dir = os.path.join(self.build_folder, 'build')
        self.run('cmake --build {0} --target install -- DESTDIR={1}'.format(build_dir, self.package_folder))

    def package_info(self):
        self.cpp_info.libs = [
            'gtest',
            'gtest_main',
            'gmock',
            'gmock_main'
        ]
