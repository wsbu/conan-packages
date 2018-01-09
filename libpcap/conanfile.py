import os

from conans import ConanFile, AutoToolsBuildEnvironment


class libpcapConan(ConanFile):
    name = 'libpcap'
    version = '1.8.0'
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
        self.run('git clone --depth=1 https://github.com/the-tcpdump-group/libpcap -b libpcap-1.8.1')

    def build(self):
        env = AutoToolsBuildEnvironment(self)

        args = [
            '--prefix', self.package_folder,
            '--with-pcap=' + self.settings.get_safe('os').lower(),
            '--with%s-libnl' % ('' if self.options.with_libnl else 'out')
        ]
        os.environ['PATH'] += os.pathsep + os.pathsep.join(self.deps_cpp_info.bindirs)
        env.configure(configure_dir=(os.path.join(self.source_folder, 'libpcap')), args=args)
        env.make(args=['-C', self.build_folder])
        env.make(args=['install'])

    def package_info(self):
        self.cpp_info.libs = [
            'pcap'
        ]

    def configure(self):
        del self.settings.compiler.libcxx
        super(libpcapConan, self).configure()
