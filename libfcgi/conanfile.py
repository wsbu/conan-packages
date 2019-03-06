import os
import shutil

from conans import ConanFile, AutoToolsBuildEnvironment, tools


class libfcgi(ConanFile):
    name = 'libfcgi'
    version = '2.4.0'
    url = 'https://github.com/wsbu/conan-packages'
    homepage = 'https://directory.fsf.org/wiki/Libfcgi'
    description = 'FastCGI is a language independent, scalable, open extension to CGI that provides high performance ' \
                  'without the limitations of server specific APIs.'
    settings = 'os', 'compiler', 'build_type', 'arch'
    license = 'FastCGI'

    scm = {
        'type': 'git',
        'url': 'git@bitbucket.org:redlionstl/libfcgi.git',
        'revision': 'RAM_4.28'
    }

    def build(self):
        os.mkdir(self.build_dir)

        args = [
            '--prefix=/usr',
        ]

        with tools.chdir(self.build_dir):
            self.auto_tools_env.configure(configure_dir=self.build_folder, args=args)
        self.auto_tools_env.make(args=['-C', self.build_dir, '-j1'])  # libfcgi's Makefile can't handle multi-threading

    def package(self):
        with tools.environment_append({'DESTDIR': self.package_folder}):
            self.auto_tools_env.install(args=['-C', self.build_dir, '-j1'])

        # DO NOT package libfcgi++ - it does not build reliably and therefore no one should use it
        base_path = os.path.join(self.package_folder, 'usr', 'lib')
        for e in os.listdir(base_path):
            if e.startswith('libfcgi++'):
                os.remove(os.path.join(base_path, e))

        src_license = os.path.join(self.source_folder, 'LICENSE.TERMS')
        license_folder = os.path.join(self.package_folder, 'etc', 'license')
        dst_license = os.path.join(license_folder, self.name)
        os.makedirs(license_folder)
        shutil.copy2(src_license, dst_license)

    def package_info(self):
        self.cpp_info.bindirs = [os.path.join('usr', 'bin')]
        self.cpp_info.includedirs = [os.path.join('usr', 'include')]
        self.cpp_info.libdirs = [os.path.join('usr', 'lib')]
        self.cpp_info.libs = ['fcgi']

    @property
    def build_dir(self):
        return os.path.join(self.build_folder, 'build')

    @property
    def auto_tools_env(self):
        return AutoToolsBuildEnvironment(self)
