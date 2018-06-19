import os

from conans import ConanFile, AutoToolsBuildEnvironment, tools


class libpcapConan(ConanFile):
    name = 'libpopt'
    version = '1.6'
    url = 'https://github.com/wsbu/conan-packages'
    description = 'the LIBpcap interface to various kernel packet capture mechanism'
    settings = 'os', 'compiler', 'build_type', 'arch'
    license = 'BSD'
    default_on_features = [
        'dependency_tracking',
        'shared',
        'fast_install',
        'libtool_lock',
        'rpath',
        'nls'
    ]
    optional_packages = [
        'with_gnu_ld',
        'with_included_gettext'
    ]

    options = {feature: [True, False] for feature in default_on_features + optional_packages}

    default_options = ['%s=True' % feature for feature in default_on_features]
    default_options += ['%s=False' % package for package in optional_packages]
    default_options = tuple(default_options)

    def source(self):
        self.run('git clone --depth=1 git@bitbucket.org:redlionstl/libpopt.git -b dev')

    def build(self):
        source_dir = os.path.join(self.build_folder, self.name, 'popt-' + self.version)
        build_dir = os.path.join(self.build_folder, 'build')
        os.mkdir(build_dir)

        args = ['--prefix=/']
        for feature in self.default_on_features:
            if not self.options.__getattr__(feature):
                args.append('--disable-' + feature.replace('_', '-'))
        for package in self.optional_packages:
            optional = '' if self.options.__getattr__(package) else '=no'
            args.append('--{0}{1}'.format(package.replace('_', '-'), optional))

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
