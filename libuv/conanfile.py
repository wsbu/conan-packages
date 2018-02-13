import os
from conans import ConanFile, AutoToolsBuildEnvironment, tools


class libuvConan(ConanFile):
    name = 'libuv'
    version = '1.18.0-1'
    url = 'https://github.com/wsbu/conan-packages'
    description = "Cross-platform asynchronous I/O"
    settings = 'os', 'compiler', 'build_type', 'arch'
    license = 'MIT'
    options = {'shared': [True, False]}
    default_options = 'shared=True'

    def source(self):
        self.run('git clone --depth=1 https://github.com/libuv/libuv -b v1.18.0')

    def build(self):
        source_dir = os.path.join(self.build_folder, 'libuv')
        build_dir = os.path.join(self.build_folder, 'build')
        os.mkdir(build_dir)

        env = AutoToolsBuildEnvironment(self)

        self.run('sh {0}/autogen.sh'.format(source_dir))

        with tools.chdir(build_dir):
            env.configure(configure_dir=source_dir, args=['--prefix', '/'])
        env.make(args=['-C', build_dir])

    def package(self):
        build_dir = os.path.join(self.build_folder, 'build')
        self.run('make -C {0} DESTDIR={1} install'.format(build_dir, self.package_folder))

    def package_info(self):
        self.cpp_info.libs = [
            'uv'
        ]

    def configure(self):
        del self.settings.compiler.libcxx
        super(libuvConan, self).configure()
