import os
from ftplib import FTP

from conans import ConanFile, tools, AutoToolsBuildEnvironment


class libxml2Conan(ConanFile):
    name = 'libxml2'
    version = '2.9.7'
    url = ''
    settings = 'os', 'compiler', 'build_type', 'arch'
    license = 'MIT'
    options = {
        'shared': [True, False],
        'python': [True, False]
    }
    default_options = 'shared=True', 'python=False'
    generators = 'cmake'

    FOLDER = name + '-' + version
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
        env = AutoToolsBuildEnvironment(self)

        args = ['--prefix', self.package_folder]
        if self.options.python:
            args.append('--with-python')
        else:
            args.append('--without-python')
        env.configure(configure_dir=self.FOLDER, args=args)
        env.make(args=['-C', self.build_folder])
        env.make(args=['install'])

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
