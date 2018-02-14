import os
from ftplib import FTP

from conans import ConanFile, tools, AutoToolsBuildEnvironment


class libxml2Conan(ConanFile):
    name = 'libxml2'
    version = '2.9.7'
    url = 'https://github.com/wsbu/conan-packages'
    settings = 'os', 'compiler', 'build_type', 'arch'
    license = 'MIT'
    options = {
        'shared': [True, False],
        'with_python': [True, False],
        'with_zlib': [True, False]
    }
    default_options = 'shared=True', 'with_python=False', 'with_zlib=True'

    FOLDER = name + '-' + version
    ARCHIVE = FOLDER + '.tar.gz'

    def configure(self):
        del self.settings.compiler.libcxx

        if self.options.with_zlib:
            self.requires('zlib/1.2.11@conan/stable')

        super(libxml2Conan, self).configure()

    def source(self):
        ftp = FTP('xmlsoft.org')
        try:
            ftp.login()
            with open(self.ARCHIVE, 'wb') as f:
                ftp.retrbinary('RETR %s/%s' % (self.name, self.ARCHIVE), f.write)
        finally:
            ftp.close()
        tools.untargz(self.ARCHIVE)
        os.remove(self.ARCHIVE)

    def build(self):
        source_dir = os.path.join(self.build_folder, self.FOLDER)
        build_dir = os.path.join(self.build_folder, 'build')
        os.mkdir(build_dir)

        args = [
            '--prefix', '/',
            '--with-python=yes' if self.options.with_python else '--without-python',
            '--with-zlib=yes' if self.options.with_zlib else '--without-zlib'
        ]
        if self.options.shared:
            args.append('--enable-shared=yes')
            args.append('--enable-static=no')
        else:
            args.append('--enable-shared=no')
            args.append('--enable-static=yes')

        env = AutoToolsBuildEnvironment(self)
        with tools.chdir(build_dir):
            env.configure(configure_dir=source_dir, args=args)
        env.make(args=['-C', build_dir])

    def package(self):
        build_dir = os.path.join(self.build_folder, 'build')
        self.run('make -C {0} DESTDIR={1} install'.format(build_dir, self.package_folder))

        # What the crap is wrong with libxml2???
        bad_root = os.path.join(self.package_folder, 'include', 'libxml2')
        good_root = os.path.join(self.package_folder, 'include', 'libxml')
        child = os.path.join(bad_root, 'libxml')
        tmp = os.path.join(self.package_folder, 'include', 'tmp')
        os.rename(child, tmp)
        os.rmdir(bad_root)
        os.rename(tmp, good_root)

    def package_info(self):
        self.cpp_info.libs = [
            'xml2'
        ]
