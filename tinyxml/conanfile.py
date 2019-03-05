import os
import shutil

from conans import ConanFile, tools


class tinyxml(ConanFile):
    name = 'tinyxml'
    version = '1.0.1'
    url = 'https://github.com/wsbu/conan-packages'
    homepage = 'http://www.grinninglizard.com/tinyxml/'
    description = 'TinyXML is a simple, small, C++ XML parser that can be easily integrating into other programs.'
    settings = 'os', 'compiler', 'build_type', 'arch', 'platform'
    license = 'See license file'

    scm = {
        'type': 'git',
        'url': 'git@bitbucket.org:redlionstl/tinyxml.git',
        'revision': '82e488fd7e9016170cc222f4a1b85dc57fdd29a0'
    }

    def build(self):
        extra_env_vars = {
            'BUILD_TARGET': str(self.settings.platform),
            'GPP': tools.get_env('CXX', 'g++')
        }
        with tools.environment_append(extra_env_vars):
            self.run('make --jobs ' + str(tools.cpu_count()))

    def package(self):
        lib_name = 'libtinyxml.so.' + self.version
        self.copy(lib_name, dst=os.path.join('usr', 'lib'))
        os.symlink(lib_name, os.path.join(self.package_folder, 'usr', 'lib', 'libtinyxml.so.1'))
        os.symlink(lib_name, os.path.join(self.package_folder, 'usr', 'lib', 'libtinyxml.so'))

        self.copy('*.h', dst=os.path.join('usr', 'include'))

        src_license = os.path.join(self.source_folder, 'COPYING')
        license_folder = os.path.join(self.package_folder, 'etc', 'license')
        dst_license = os.path.join(license_folder, self.name)
        os.makedirs(license_folder)
        shutil.copy2(src_license, dst_license)

    def package_info(self):
        self.cpp_info.libdirs = [os.path.join('usr', 'lib')]
        self.cpp_info.includedirs = [os.path.join('usr', 'include')]
        self.cpp_info.libs = ['tinyxml']
