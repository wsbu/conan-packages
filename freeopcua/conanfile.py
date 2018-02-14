import os
from conans import ConanFile, CMake, tools


class freeopcuaConan(ConanFile):
    name = 'freeopcua'
    version = '0.0.1-1'
    url = 'https://github.com/wsbu/conan-packages'
    description = 'Open Source C++ OPC-UA Server and Client Library'
    settings = 'os', 'compiler', 'build_type', 'arch'
    license = 'LGPL-3.0'
    options = {
        'shared': [True, False],
        'build_python': [True, False],
        'build_client': [True, False],
        'build_server': [True, False]
    }
    default_options = 'shared=True', \
                      'build_python=False', \
                      'build_client=False', \
                      'build_server=True'
    generators = 'cmake'

    requires = 'boost/1.65.1-1@wsbu/stable', ('googletest/1.8.0-1@wsbu/stable', 'private')

    def configure(self):
        self.options['Boost'].shared = self.options.shared

    def source(self):
        self.run('git clone --depth=1 https://github.com/wsbu/freeopcua')

    def build(self):
        source_dir = os.path.join(self.build_folder, 'freeopcua')
        build_dir = os.path.join(self.build_folder, 'build')

        # Without this, CMake won't know how to find the dependencies that Conan is trying to inject
        tools.replace_in_file(os.path.join(source_dir, 'CMakeLists.txt'), 'project(freeopcua)',
                              '''project(freeopcua)
include("{0}/conanbuildinfo.cmake")
conan_basic_setup()'''.format(self.build_folder))

        # Installer is broken... patch it
        tools.replace_in_file(os.path.join(source_dir, 'CMakeLists.txt'),
                              'DESTINATION "${CMAKE_INSTALL_PREFIX}/', 'DESTINATION "')

        definitions = {
            'BUILD_PYTHON': 'ON' if self.options.build_python else 'OFF',
            'BUILD_CLIENT': 'ON' if self.options.build_client else 'OFF',
            'BUILD_SERVER': 'ON' if self.options.build_server else 'OFF'
        }

        cmake = CMake(self)
        cmake.definitions['CMAKE_INSTALL_PREFIX'] = '/'
        cmake.configure(source_dir=source_dir, build_dir=build_dir, defs=definitions)
        cmake.build()

    def package(self):
        build_dir = os.path.join(self.build_folder, 'build')
        self.run('cmake --build {0} --target install -- DESTDIR={1}'.format(build_dir, self.package_folder))

    def package_info(self):
        self.cpp_info.libs = [
            'opcuaclient',
            'opcuaserver',
            'opcuaprotocol',
            'opcuacore'
        ]
        self.cpp_info.libdirs = ['lib', 'lib/static']
