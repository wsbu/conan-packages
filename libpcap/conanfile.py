import os

from conans import ConanFile, AutoToolsBuildEnvironment, tools


class libpcapConan(ConanFile):
    name = 'libpcap'
    version = '1.8.1'
    url = 'https://github.com/wsbu/conan-packages'
    description = 'the LIBpcap interface to various kernel packet capture mechanism'
    settings = 'os', 'compiler', 'build_type', 'arch'
    license = 'BSD'
    options = {
        'shared': [True, False],
        'with_libnl': [True, False]
    }
    default_options = 'shared=True', 'with_libnl=False'
    generators = 'cmake'

    def source(self):
        self.run('git clone --depth=1 https://github.com/the-tcpdump-group/libpcap -b libpcap-%s' % self.version)

    def build(self):
        source_dir = os.path.join(self.build_folder, 'libpcap')
        build_dir = os.path.join(self.build_folder, 'build')
        os.mkdir(build_dir)

        args = [
            '--prefix=/',
            '--with-pcap=' + self.settings.get_safe('os').lower(),
            '--with%s-libnl' % ('' if self.options.with_libnl else 'out')
        ]

        env = AutoToolsBuildEnvironment(self)
        with tools.chdir(build_dir):
            env.configure(configure_dir=source_dir, args=args)
        env.make(args=['-C', build_dir])

    def package(self):
        build_dir = os.path.join(self.build_folder, 'build')
        self.run('make -C {0} DESTDIR={1} install'.format(build_dir, self.package_folder))

    def package_info(self):
        self.cpp_info.libs = [
            'pcap'
        ]

    def configure(self):
        del self.settings.compiler.libcxx
        super(libpcapConan, self).configure()
