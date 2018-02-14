import os
from conans import ConanFile, CMake, tools


class OpcfUaCConan(ConanFile):
    name = 'opcf-ua-c'
    version = '1.03.341'
    url = 'https://github.com/wsbu/conan-packages'
    description = 'UA ANSI C Stack reference implementation for OPC UA'
    settings = 'os', 'compiler', 'build_type', 'arch'
    license = 'OPC Foundation Corporate Members: RCL; Everybody else: GPL 2.0'
    options = {
        'shared': [True, False]
    }
    default_options = 'shared=True'
    generators = 'cmake'

    requires = 'OpenSSL/1.1.0g@wsbu/stable'

    def configure(self):
        del self.settings.compiler.libcxx
        super(OpcfUaCConan, self).configure()

    def source(self):
        self.run('git clone --depth=1 git@bitbucket.org:redlionstl/{0}.git -b {1}'.format(self.name, self.version))

    def build(self):
        source_dir = os.path.join(self.build_folder, self.name)
        build_dir = os.path.join(self.build_folder, 'build')

        # Without this, CMake won't know how to find the dependencies that Conan is trying to inject
        tools.replace_in_file(os.path.join(source_dir, 'CMakeLists.txt'), 'project(UA-AnsiC)',
                              '''project(UA-AnsiC)
include("{0}/conanbuildinfo.cmake")
conan_basic_setup()'''.format(self.build_folder))

        cmake = CMake(self)
        cmake.definitions['CMAKE_INSTALL_PREFIX'] = '/'
        cmake.configure(source_dir=source_dir, build_dir=build_dir)
        cmake.build()

    def package(self):
        self.copy('*', src='build/lib', dst='lib')
        self.copy('*', src='build/bin', dst='bin')
        self.copy('*.h', src=self.name, dst='include')

    def package_info(self):
        self.cpp_info.libs = ['uastack']
