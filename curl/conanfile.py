import os

import shutil
from conans import ConanFile, tools, AutoToolsBuildEnvironment


class CurlConan(ConanFile):
    name = 'curl'
    version = '7.28.1'
    url = 'https://github.com/wsbu/conan-packages'
    settings = 'os', 'compiler', 'build_type', 'arch'
    license = 'see COPYING file'

    ARCHIVE = '{0}-{1}.tar.gz'.format(name, version)
    SOURCE_DIR = '{0}-{1}'.format(name, version)

    options = {
        'shared':     [True, False],
        'ldap':       [True, False],
        'ldaps':      [True, False],
        'with_axtls': [True, False],
        'with_ssl':   [True, False],
        'with_zlib':  [True, False]
    }
    default_options = 'shared=True', \
                      'ldap=False', \
                      'ldaps=False', \
                      'with_axtls=False', \
                      'with_ssl=True', \
                      'with_zlib=True'

    def requirements(self):
        if self.options.with_zlib:
            self.requires("zlib/1.2.11@conan/stable")
        if self.options.with_ssl:
            self.requires("OpenSSL/1.0.2n@conan/stable")
        if self.options.with_axtls:
            raise Exception('axtls not supported')

    def source(self):
        tools.download('https://curl.haxx.se/download/{0}'.format(self.ARCHIVE), self.ARCHIVE)
        tools.untargz(self.ARCHIVE)
        os.remove(self.ARCHIVE)

    def build(self):

        args = ['--prefix=/']

        if self.options.shared:
            args.append('--enable-shared=yes')
            args.append('--enable-static=no')
        else:
            args.append('--enable-shared=no')
            args.append('--enable-static=yes')

        args.append('--enable-ldap' if self.options.ldap else '--disable-ldap')
        args.append('--enable-ldaps' if self.options.ldaps else '--disable-ldaps')
        args.append('--with-axtls' if self.options.with_axtls else '--without-axtls')
        args.append('--with-ssl' if self.options.with_ssl else '--without-ssl')
        args.append('--with-zlib' if self.options.with_zlib else '--without-zlib')

        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)
        os.makedirs(self.build_dir)
        with tools.chdir(self.build_dir):
            env = AutoToolsBuildEnvironment(self)
            env.configure(configure_dir=self.source_dir, args=args)
            env.make()

    def package(self):
        self.run('make -C {0} DESTDIR={1} install'.format(self.build_dir, self.package_folder))

    def package_info(self):
        self.cpp_info.libs = ['curl']

    def configure(self):
        del self.settings.compiler.libcxx

    @property
    def build_dir(self):
        return os.path.join(self.build_folder, 'build')

    @property
    def source_dir(self):
        return os.path.join(self.build_folder, self.SOURCE_DIR)
