import os

from conans import ConanFile, CMake, tools


class CppZmq(ConanFile):
    name = 'cppzmq'
    version = '4.3.0'
    url = 'https://github.com/wsbu/conan-packages'
    homepage = 'https://github.com/zeromq/cppzmq'
    description = 'C++ binding for libzmq'
    settings = 'os', 'compiler', 'build_type', 'arch'
    license = 'MIT'
    options = {
        'enable_drafts': [True, False],
        'cppzmq_build_tests': [True, False]
    }
    default_options = (
        'enable_drafts=False',
        'cppzmq_build_tests=True'
    )

    generators = 'cmake'

    scm = {
        'type': 'git',
        'url': 'git@bitbucket.org:redlionstl/cppzmq.git',
        'revision': 'v' + version
    }

    requires = 'libzmq/[^4.0.0]@wsbu/stable'

    def build(self):
        # Without this, CMake won't know how to find the dependencies that Conan is trying to inject
        tools.replace_in_file(os.path.join(self.build_folder, 'CMakeLists.txt'), 'find_package(ZeroMQ QUIET)',
                              '''include("{0}/conanbuildinfo.cmake")
conan_basic_setup(TARGETS)

find_package(ZeroMQ QUIET)'''.format(self.build_folder))

        cmake = self.cmake
        cmake.build()
        if self.options.cppzmq_build_tests:
            cmake.test()

    def package(self):
        self.cmake.install()

    @property
    def cmake(self):
        definitions = {
            'ENABLE_DRAFTS': 'ON' if self.options.enable_drafts else 'OFF',
            'CPPZMQ_BUILD_TESTS': 'ON' if self.options.cppzmq_build_tests else 'OFF'
        }

        cmake = CMake(self)
        cmake.configure(defs=definitions, source_folder=self.build_folder,
                        build_folder=os.path.join(self.build_folder, 'build'))
        return cmake
