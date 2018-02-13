import multiprocessing
import os

from conans import ConanFile


class libtermcapConan(ConanFile):
    name = 'libtermcap'
    version = '2.0.8-1'
    short_version = version.split('-')[0]
    url = 'https://github.com/wsbu/conan-packages'
    license = 'GNU'
    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = 'shared=True'

    relative_source = os.path.join(name, 'termcap-' + short_version)

    def source(self):
        self.run('git clone --depth=1 git@bitbucket.org:redlionstl/libtermcap.git')

    def build(self):
        self.run('make -C {0} -j {1}'.format(self.folder, multiprocessing.cpu_count()))

    def package(self):
        if self.options.shared:
            os.symlink('libtermcap.so.' + self.short_version,
                       os.path.join(self.folder, 'libtermcap.so.' + self.short_version.split('.')[0]))
            os.symlink('libtermcap.so.' + self.short_version, os.path.join(self.folder, 'libtermcap.so'))
            self.copy('*so*', dst='usr/lib', src=self.relative_source)
        else:
            self.copy('*a*', dst='usr/lib', src=self.relative_source)
        self.copy('*.h*', dst='usr/include', src=self.relative_source)

        if os.path.exists(os.path.join(self.folder, 'COPYING')):
            os.rename(os.path.join(self.folder, 'COPYING'), os.path.join(self.folder, 'libtermcap'))
            self.copy('libtermcap', dst='etc/license', src=self.relative_source)

    def package_info(self):
        self.cpp_info.rootdir = 'usr'
        self.cpp_info.libdirs = ['usr/lib']
        self.cpp_info.includedirs = ['usr/include']
        self.cpp_info.libs = ['termcap']

    def configure(self):
        del self.settings.compiler.libcxx

    @property
    def folder(self):
        return os.path.join(self.build_folder, self.relative_source)
