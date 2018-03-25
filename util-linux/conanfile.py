import os

from conans import ConanFile, AutoToolsBuildEnvironment, tools, RunEnvironment


class UtilLinuxConan(ConanFile):
    name = 'util-linux'
    version = '1.18.0'
    url = 'https://github.com/wsbu/conan-packages'
    description = "Linux utilities"
    settings = 'os', 'compiler', 'build_type', 'arch'
    license = 'GNU GPLv2'

    def source(self):
        self.run('git clone --depth=1 git@bitbucket.org:redlionstl/util-linux.git')

    def build(self):
        source_dir = os.path.join(self.build_folder, self.name)
        build_dir = os.path.join(self.build_folder, 'build')
        os.mkdir(build_dir)

        env = AutoToolsBuildEnvironment(self)

        with tools.environment_append(RunEnvironment(self).vars):
            self.run('sh {0}/autogen.sh'.format(source_dir))

            with tools.chdir(build_dir):
                env.configure(configure_dir=source_dir, args=['--disable-use-tty-group'])
            env.make(args=['-C', build_dir, 'LDFLAGS=-Wl,-rpath-link=' + os.path.join(build_dir, '.libs')])

    def package(self):
        build_dir = os.path.join(self.build_folder, 'build')
        self.run('make -C {0} DESTDIR={1} install'.format(build_dir, self.package_folder))

    def package_info(self):
        self.cpp_info.includedirs = ['include', 'usr/include']
        self.cpp_info.libdirs = ['lib', 'usr/lib']
        self.cpp_info.bindirs = ['bin', 'sbin', 'usr/bin', 'usr/sbin']

    def configure(self):
        del self.settings.compiler.libcxx
        super(UtilLinuxConan, self).configure()
