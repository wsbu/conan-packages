import os
import shutil

from conans import ConanFile, tools


class ArptablesConan(ConanFile):
    name = 'arptables'
    version = '0.0.4-1'
    short_version = version.split('-')[0]
    url = 'https://github.com/wsbu/conan-packages'
    settings = 'os', 'compiler', 'build_type', 'arch'
    license = 'GNU'

    def source(self):
        self.run('git clone --depth 1 git@bitbucket.org:redlionstl/wsbu-arptables.git')

    def build(self):
        self.run('make -C {0} -j{1}'.format(self.folder, tools.cpu_count()))

    def package(self):
        self.run('make -C {0} -j{1} DESTDIR={2} PREFIX=/usr install'.format(self.folder, tools.cpu_count(),
                                                                            self.package_folder))
        license_dst_dir = os.path.join(self.package_folder, 'etc', 'license')
        os.makedirs(license_dst_dir)
        shutil.copy2(os.path.join(self.folder, 'LICENCE'), os.path.join(license_dst_dir, self.name))

    def package_info(self):
        self.cpp_info.bindirs = ['usr/sbin']

    def configure(self):
        del self.settings.compiler.libcxx

    @property
    def relative_folder(self):
        return 'wsbu-' + self.name

    @property
    def folder(self):
        return os.path.join(self.build_folder, self.relative_folder)
