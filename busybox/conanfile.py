import os
import shutil
import subprocess

from conans import ConanFile, tools


class BusyboxConan(ConanFile):
    name = 'busybox'
    version = '1.24.2-1'
    license = 'GNU GPL'
    url = 'https://github.com/wsbu/conan-packages'
    description = "Swiss army knife of embedded Linux"
    settings = 'os', 'compiler', 'build_type', 'arch', 'platform'
    options = {
        'verbose': [True, False]
    }
    default_options = 'verbose=False'
    generators = 'gcc'

    ARCHITECTURE_MAP = {
        'armv7hf': 'arm',
        'x86_64': 'x86',
        'x86': 'x86'
    }

    def source(self):
        self.run('git clone --depth=1 git@bitbucket.org:redlionstl/busybox.git')

    def build(self):
        self._check_version()
        cpu_count = tools.cpu_count()
        platform = self.settings.get_safe('platform')

        make_flags = self._get_make_flags()

        preferred_config_filename = platform + '_defconfig'
        preferred_config = os.path.join(self.folder, 'configs', preferred_config_filename)
        if os.path.exists(preferred_config):
            shutil.copy2(preferred_config, os.path.join(self.folder, '.config'))
        else:
            self.output.warn('Config not found ({0}). Generating default config.'.format(preferred_config_filename))
            self.run('make -j{0} -C {1} {2} defconfig'.format(cpu_count, self.folder, make_flags))
        self.run('make -j{0} -C {1} {2} busybox'.format(cpu_count, self.folder, make_flags))

    def configure(self):
        del self.settings.compiler.libcxx
        super(BusyboxConan, self).configure()

    def package(self):
        self.run('make -j{0} -C {1} {2} CONFIG_PREFIX={3} install'
                 .format(tools.cpu_count(), self.folder, self._get_make_flags(), self.package_folder))

    def _check_version(self):
        # Ensure we don't have a version mismatch
        p = subprocess.Popen(['make', '-C', self.folder, '--no-print-directory', 'kernelversion'],
                             stdout=subprocess.PIPE)
        stdout = p.communicate()[0]
        make_version = stdout.decode().strip()
        conan_version = self.version.split('-')[0]  # Strip Conan's recipe version
        error_msg = 'Version from build system should match Conan version: Make={0}, Conan={1}' \
            .format(make_version, conan_version)
        assert make_version == conan_version, error_msg

    def _get_make_flags(self):
        flags = ['ARCH={0}'.format(self.ARCHITECTURE_MAP[self.settings.get_safe('arch')])]
        if tools.cross_building(self.settings):
            flags.append('CROSS_COMPILE={0}'.format(os.environ['CC'][:-3]))
        if self.options.verbose:
            flags.append('V=1')
        with open(os.path.join(self.build_folder, 'conanbuildinfo.gcc'), 'r') as flags_file:
            x = flags_file.read()
            self.output.info('FLAGS = "{0}"'.format(x))
            flags.append("CFLAGS='{0}'".format(x))
        return ' '.join(flags)

    @property
    def relative_folder(self):
        return self.name

    @property
    def folder(self):
        return os.path.join(self.build_folder, self.relative_folder)
