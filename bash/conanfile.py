import os

import shutil
from conans import ConanFile, tools, AutoToolsBuildEnvironment


class BashConan(ConanFile):
    name = 'bash'
    version = '3.2-1'
    short_version = version.split('-')[0]
    url = 'https://github.com/wsbu/conan-packages'
    settings = 'os', 'compiler', 'build_type', 'arch'
    license = 'GNU'
    default_on_features = [
        'alias',
        'arith_for_command',
        'array_variables',
        'bang_history',
        'brace_expansion',
        'command_timing',
        'cond_command',
        'cond_regexp',
        'debugger',
        'directory_stack',
        'disabled_builtins',
        'dparen_arithmetic',
        'extended_glob',
        'help_builtin',
        'history',
        'job_control',
        'multibyte',
        'net_redirections',
        'process_substitution',
        'progcomp',
        'prompt_string_decoding',
        'readline',
        'restricted',
        'select',
        'separate_helpfiles',
        'single_help_strings',
        'strict_posix_default',
        'usg_echo_default',
        'xpg_echo_default',
        'mem_scramble',
        'profiling',
        'static_link'
    ]
    default_off_features = [
        'largefile',
        'nls',
        'rpath'
    ]
    optional_packages = [
        'with_lispdir',
        'with_afs',
        'with_bash_malloc',
        'with_curses',
        'with_installed_readline',
        'with_purecov',
        'with_purify',
        'with_gnu_ld'
    ]

    options = {feature: [True, False] for feature in default_on_features + default_off_features + optional_packages}

    default_options = ['%s=True' % feature for feature in default_on_features]
    default_options += ['%s=False' % feature for feature in default_off_features]
    default_options += ['%s=False' % package for package in optional_packages]
    default_options = tuple(default_options)

    requires = 'libtermcap/2.0.8-1@wsbu/stable'

    def source(self):
        self.run('git clone --depth 1 git@bitbucket.org:redlionstl/bash.git')

    def build(self):
        starting_flags = os.environ['CPPFLAGS'] if 'CPPFLAGS' in os.environ else ''
        extra_flags = ['-I%s' % include_dir for include_dir in self.deps_cpp_info['libtermcap'].includedirs]
        os.environ['CPPFLAGS'] = starting_flags + ' ' + ' '.join(extra_flags)

        args = ['--prefix', '/usr']
        for feature in self.default_on_features:
            if not self.options.__getattr__(feature):
                args.append('--disable-' + feature.replace('_', '-'))
        for feature in self.default_off_features:
            if self.options.__getattr__(feature):
                args.append('--enable-' + feature.replace('_', '-'))
        for package in self.optional_packages:
            optional = '' if self.options.__getattr__(package) else 'out'
            args.append('--with{0}-{1}'.format(optional, package.replace('_', '-')))

        shutil.copy2(os.path.join(self.build_folder, 'bash', 'config', 'config.guess'), os.path.join(self.folder))
        shutil.copy2(os.path.join(self.build_folder, 'bash', 'config', 'config.sub'), os.path.join(self.folder))
        env = AutoToolsBuildEnvironment(self)
        with tools.chdir(self.folder):
            env.configure(configure_dir=self.folder, args=args)
            # This old version of bash has a race condition when built with multiple CPU cores.
            # Don't do it...
            env.make(args=['-j1'])

    def package(self):
        src_bash_exe = os.path.join(self.folder, 'bash')
        dst_folder = os.path.join(self.package_folder, 'bin')
        dst_bash_exe = os.path.join(dst_folder, 'bash')

        os.mkdir(dst_folder)
        shutil.copy2(src_bash_exe, dst_bash_exe)
        if 'CC' in os.environ:
            if os.environ['CC'].endswith('gcc'):
                prefix = os.environ['CC'][:-3]
                strip = prefix + 'strip'
            else:
                raise Exception("I don't know how to strip executables from this compiler: " + os.environ['CC'])
        else:
            strip = 'strip'
        self.run(strip + ' ' + dst_bash_exe)

        src_license = os.path.join(self.folder, 'COPYING')
        license_folder = os.path.join(self.package_folder, 'etc', 'license')
        dst_license = os.path.join(license_folder, 'bash')
        os.makedirs(license_folder)
        shutil.copy2(src_license, dst_license)

    def package_info(self):
        self.cpp_info.rootdir = os.path.join(self.package_folder, 'usr')

    def configure(self):
        del self.settings.compiler.libcxx

    @property
    def folder(self):
        return os.path.join(self.build_folder, 'bash', 'bash-' + self.short_version)
