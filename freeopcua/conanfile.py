from conans import ConanFile, CMake, tools


class freeopcuaConan(ConanFile):
    name = 'freeopcua'
    version = '1.8.0'
    url = 'http://freeopcua.github.io/'
    description = 'Open Source C++ OPC-UA Server and Client Library'
    settings = 'os', 'compiler', 'build_type', 'arch'
    license = 'LGPL-3.0'
    options = {
        'shared': [True, False],
        'build_python': [True, False],
        'build_client': [True, False],
        'build_server': [True, False]
    }
    default_options = 'shared=False', \
                      'build_python=False', \
                      'build_client=False', \
                      'build_server=True'
    generators = 'cmake'

    requires = 'Boost/1.64.0@conan/stable', 'googletest/1.8.0@wsbu/testing'

    def source(self):
        self.run('git clone --depth=1 https://github.com/FreeOpcUa/freeopcua')

        # Without this, CMake won't know how to find the dependencies that Conan is trying to inject
        tools.replace_in_file('freeopcua/CMakeLists.txt', 'project(freeopcua)',
                              '''project(freeopcua)
include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
conan_basic_setup(TARGETS)''')

    def build(self):
        definitions = {
            'BUILD_PYTHON': 'ON' if self.options.build_python else 'OFF',
            'BUILD_CLIENT': 'ON' if self.options.build_client else 'OFF',
            'BUILD_SERVER': 'ON' if self.options.build_server else 'OFF'
        }

        cmake = CMake(self)
        cmake.configure(source_dir='freeopcua', defs=definitions)
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = [
            'opcuaclient',
            'opcuaserver',
            'opcuaprotocol',
            'opcuacore'
        ]
