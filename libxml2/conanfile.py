import os
from ftplib import FTP

from conans import ConanFile, tools, AutoToolsBuildEnvironment


class libxml2Conan(ConanFile):
    name = 'libxml2'
    version = '2.9.7+1'
    url = 'https://github.com/wsbu/conan-packages'
    settings = 'os', 'compiler', 'build_type', 'arch'
    license = 'MIT'
    options = {
        'shared': [True, False],
        'python': [True, False]
    }
    default_options = 'shared=True', 'python=False'

    FOLDER = name + '-' + version.split('+')[0]
    ARCHIVE = FOLDER + '.tar.gz'

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

        args = ['--prefix', '/']
        if self.options.python:
            args.append('--with-python')
        else:
            args.append('--without-python')

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

    def configure(self):
        del self.settings.compiler.libcxx
        super(libxml2Conan, self).configure()
