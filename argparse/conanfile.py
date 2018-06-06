import os
import shutil

from conans import ConanFile


class ArgparseConan(ConanFile):
    name = 'argparse'
    version = '0.0.1'
    license = 'See License File'
    url = 'https://bitbucket.org/redlionstl/argparse.git'
    description = 'Opensource C++ argument parsing library'

    def source(self):
        self.run('git clone git@bitbucket.org:redlionstl/argparse.git .')
        self.run('git reset --hard 43edb8a')  # No tags exist in the repo

    def package(self):
        self.copy('*.hpp', dst='usr/include')
        license_destination_dir = os.path.join(self.package_folder, 'usr/etc/license')
        os.makedirs(license_destination_dir)
        shutil.copy2(os.path.join(self.source_folder, 'LICENSE'), os.path.join(license_destination_dir, self.name))

    def package_info(self):
        self.cpp_info.includedirs = ['usr/include']
