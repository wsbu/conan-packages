import os
from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment


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

    def source(self):
        self.run('git clone --depth=1 https://github.com/GNOME/libxml2 -b v%s' % self.version)

    def build(self):
        env = AutoToolsBuildEnvironment(self)

        src = os.path.join(self.source_folder, 'libxml2')
        self.run('env NOCONFIGURE=1 sh autogen.sh', cwd=src)

        args = ['--prefix', self.package_folder]
        if self.options.python:
            args.append('--with-python')
        else:
            args.append('--without-python')
        env.configure(configure_dir=src, args=args)
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
