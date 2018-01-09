import os
from conans import ConanFile, AutoToolsBuildEnvironment


class libuvConan(ConanFile):
    name = 'libuv'
    version = '1.18.0'
    url = 'https://github.com/libuv/libuv'
    description = "Cross-platform asynchronous I/O"
    settings = 'os', 'compiler', 'build_type', 'arch'
    license = 'MIT'
    options = {'shared': [True, False]}
    default_options = 'shared=True'

    def source(self):
        self.run('git clone --depth=1 https://github.com/libuv/libuv -b v1.18.0')

    def build(self):
        env = AutoToolsBuildEnvironment(self)

        src = os.path.join(self.source_folder, 'libuv')
        os.environ['PATH'] += os.pathsep + os.pathsep.join(self.deps_cpp_info.bindirs)
        self.run('sh {0}/autogen.sh'.format(src))
        env.configure(configure_dir=src, args=['--prefix', self.package_folder])
        env.make(args=['-C', self.build_folder])
        env.make(args=['install'])

    def package_info(self):
        self.cpp_info.libs = [
            'uv'
        ]

    def configure(self):
        del self.settings.compiler.libcxx
        super(libuvConan, self).configure()
