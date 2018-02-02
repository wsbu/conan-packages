import os

import shutil
from conans import ConanFile, tools


class AgettyConan(ConanFile):
    name = 'agetty'
    version = '1.29+1'
    short_version = version.split('+')[0]
    url = 'https://github.com/wsbu/conan-packages'
    settings = 'os', 'compiler', 'build_type', 'arch'
    license = 'GNU'

    def source(self):
        self.run('git clone --depth 1 git@bitbucket.org:redlionstl/agetty.git')

    def build(self):
        self.run('make -C {0} -j{1}'.format(self.folder, tools.cpu_count()))

    def package(self):
        self.copy(self.name, dst='bin', src=self.relative_folder)

        license_destination_dir = os.path.join(self.package_folder, 'usr/etc/license')
        os.makedirs(license_destination_dir)
        shutil.copy2(os.path.join(self.folder, 'LICENCE'), os.path.join(license_destination_dir, self.name))

    def configure(self):
        del self.settings.compiler.libcxx

    @property
    def relative_folder(self):
        return os.path.join(self.name, self.name + '-' + self.short_version)

    @property
    def folder(self):
        return os.path.join(self.build_folder, self.relative_folder)
