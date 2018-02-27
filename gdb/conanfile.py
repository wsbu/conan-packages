import os

import shutil
from conans import ConanFile, tools, AutoToolsBuildEnvironment


class GdbConan(ConanFile):
    name = 'gdbserver'
    version = '8.1'
    url = 'https://github.com/wsbu/conan-packages'
    settings = 'os', 'compiler', 'build_type', 'arch'
    license = 'GNU'

    ARCHIVE = 'gdb-{0}.tar.gz'.format(version)

    def source(self):
        tools.download('https://ftp.gnu.org/gnu/gdb/' + self.ARCHIVE, self.ARCHIVE)
        tools.untargz(self.ARCHIVE)
        os.remove(self.ARCHIVE)

    def build(self):
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)
        os.makedirs(self.build_dir)
        with tools.chdir(self.build_dir):
            env = AutoToolsBuildEnvironment(self)
            env.configure(configure_dir=self.source_dir, args=['--prefix=/'])
            env.make()

    def package(self):
        self.run('make -C {0} DESTDIR={1} install'.format(self.build_dir, self.package_folder))

    def configure(self):
        del self.settings.compiler.libcxx

    @property
    def relative_folder(self):
        return os.path.join('gdb-' + self.version, 'gdb', self.name)

    @property
    def source_dir(self):
        return os.path.join(self.build_folder, self.relative_folder)

    @property
    def build_dir(self):
        return os.path.join(self.build_folder, 'build')
