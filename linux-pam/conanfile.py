import os

from conans import ConanFile, AutoToolsBuildEnvironment, tools


class LinuxPamConan(ConanFile):
    name = 'linux-pam'
    version = '1.2.1'
    url = 'https://github.com/wsbu/conan-packages'
    description = 'Pluggable Authentication Modules for Linux'
    settings = 'os', 'compiler', 'build_type', 'arch'
    license = 'See COPYING'

    def source(self):
        self.run('git clone --depth=1 git@bitbucket.org:redlionstl/wsbu-linux-pam.git -b RAM_4.28')

    def build(self):
        configure_opts = [
            '--prefix=/usr',
            '--disable-regenerate-docu',
            '--disable-cracklib',
            '--disable-prelude'
        ]

        env = AutoToolsBuildEnvironment(self)
        with tools.chdir(self.folder):
            self.run('sh {0}/autogen.sh'.format(self.folder))
            env.configure(configure_dir=self.folder, args=configure_opts)
            env.make()

    def package(self):
        self.run('make -C {0} DESTDIR={1} install'.format(self.folder, self.package_folder))

    def package_info(self):
        self.cpp_info.libs = [
            'pamc',
            'pam',
            'pam_misc'
        ]
        self.cpp_info.libdirs = ['usr/lib', 'usr/lib/security']
        self.cpp_info.includedirs = ['usr/include']
        self.cpp_info.bindirs = ['sbin']

    @property
    def folder(self):
        return os.path.join(self.build_folder, 'wsbu-' + self.name)
