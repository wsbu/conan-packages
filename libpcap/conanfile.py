import os
from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment


class libpcapConan(ConanFile):
    name = 'libpcap'
    version = '1.18.0'
    description = 'the LIBpcap interface to various kernel packet capture mechanism'
    settings = 'os', 'compiler', 'build_type', 'arch'
    license = 'BSD'
    options = {'shared': [True, False]}
    default_options = 'shared=True'
    generators = 'cmake'

    def source(self):
        self.run('git clone --depth=1 https://github.com/the-tcpdump-group/libpcap -b libpcap-1.8.1')

    def build(self):
        env = AutoToolsBuildEnvironment(self)

        env.configure(configure_dir=(os.path.join(self.source_folder, 'libpcap')),
                      args=['--prefix', self.package_folder])
        env.make(args=['-C', self.build_folder])
        env.make(args=['install'])

    def package_info(self):
        self.cpp_info.libs = [
            'pcap'
        ]

    def configure(self):
        del self.settings.compiler.libcxx
        super(libpcapConan, self).configure()
