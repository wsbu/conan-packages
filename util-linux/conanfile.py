import os

from conans import ConanFile, AutoToolsBuildEnvironment, tools


class UtilLinuxConan(ConanFile):
    name = 'util-linux'
    version = '2.30.2'
    url = 'https://github.com/wsbu/conan-packages'
    description = "Linux utilities"
    settings = 'os', 'compiler', 'build_type', 'arch'
    license = 'GNU GPLv2'

    requires = 'linux-pam/1.2.1@wsbu/stable'

    def source(self):
        self.run('git clone --depth=1 git@bitbucket.org:redlionstl/util-linux.git -b v2.30.2')

    def build(self):
        ldflags = [
            '-Wl,-rpath-link={0}'.format(os.path.join(self.folder, '.libs'))
        ]
        cflags = []

        for requirement_name in self.requires:
            requirement = self.deps_cpp_info[requirement_name]
            for lib_dir in requirement.libdirs:
                ldflags.append('-L' + os.path.join(requirement.rootpath, lib_dir))
            for include_dir in requirement.includedirs:
                cflags.append('-I' + os.path.join(requirement.rootpath, include_dir))

        extra_environment_vars = {
            'LDFLAGS': ' '.join(ldflags),
            'CFLAGS': ' '.join(cflags),
            'CPPFLAGS': ' '.join(cflags)
        }

        with tools.environment_append(extra_environment_vars):
            self.run('sh {0}/autogen.sh'.format(self.folder))
            env = AutoToolsBuildEnvironment(self)
            with tools.chdir(self.folder):
                env.configure(configure_dir=self.folder, args=['--disable-use-tty-group', '--prefix=/'])
            env.make(args=['-C', self.folder])

    def package(self):
        self.run('make -C {0} DESTDIR={1} install'.format(self.folder, self.package_folder))

    def package_info(self):
        self.cpp_info.includedirs = ['include', 'usr/include']
        self.cpp_info.libdirs = ['lib', 'usr/lib']
        self.cpp_info.bindirs = ['bin', 'sbin', 'usr/bin', 'usr/sbin']

    def configure(self):
        del self.settings.compiler.libcxx
        super(UtilLinuxConan, self).configure()

    @property
    def folder(self):
        return os.path.join(self.build_folder, self.name)
