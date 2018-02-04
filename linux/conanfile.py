import os
import shutil
import subprocess

from conans import ConanFile, tools


class LinuxConan(ConanFile):
    name = 'linux'
    version = '4.4.36+1'
    license = 'GNU GPL'
    url = 'https://github.com/wsbu/conan-packages'
    description = "Kernel modules and headers (and maybe source)"
    settings = 'compiler', 'build_type', 'arch', 'platform'
    options = {
        'install_source': [True, False]
    }
    default_options = 'install_source=False'

    ARCHITECTURE_MAP = {
        'armv7hf': 'arm',
        'x86_64': 'x86',
        'x86': 'x86'
    }
    LOAD_ADDR_MAP = {
        'sitara': '80008000'
    }

    def source(self):
        self.run('git clone --depth=1 git@bitbucket.org:redlionstl/mbl-sw-nt24k-linux-kernel')

    def build(self):
        # Without this, the kernel thinks that the source has been modified and tries to append a '+' to the version
        # number
        self.run('touch {0}'.format(os.path.join(self.folder, '.scmversion')))

        kernel_version = self._check_version()
        cpu_count = tools.cpu_count()
        platform = self.settings.get_safe('platform')
        common_make_flags = self._get_make_flags()

        # Before compiling everything, copy the source code into the package
        if self.options.install_source:
            shutil.copytree(os.path.join(self.source_folder, self.relative_folder),
                            os.path.join(self.package_folder, 'usr/src/kernels', kernel_version))

        self.run('make -C {0} -j{1} {2} {3}_defconfig'.format(self.folder, cpu_count, common_make_flags, platform))
        load_address_arg = 'LOADADDR=%s' % (self.LOAD_ADDR_MAP[platform] if platform not in ['x86', 'x86_64'] else '')

        if self.settings.get_safe('arch') not in ['x86', 'x86_64']:
            self.run('make -C {0} -j{1} {2} {3} uImage'.format(self.folder, cpu_count, common_make_flags,
                                                               load_address_arg))
        self.run('make -C {0} -j{1} {2} modules'.format(self.folder, cpu_count, common_make_flags))

    def package(self):
        kernel_version = self._check_version()
        cpu_count = tools.cpu_count()
        arch = self.settings.get_safe('arch')
        common_make_flags = self._get_make_flags()

        self.run('env')
        self.run('make -C {0} -j{1} {2} INSTALL_HDR_PATH={3} INSTALL_MOD_PATH={3} headers_install modules_install'
                 .format(self.folder, cpu_count, common_make_flags, self.package_folder))

        self.output.info('Removing symlinks from package directory to source/build directory')
        os.remove(os.path.join(self.package_folder, 'lib', 'modules', kernel_version, 'build'))
        src_link = os.path.join(self.package_folder, 'lib', 'modules', kernel_version, 'source')
        os.remove(src_link)
        if self.options.install_source:
            self.output.info('Creating better symlink from package directory to source directory')
            os.symlink(os.path.join('../../../usr/src/kernels', kernel_version), src_link)

        if self.settings.get_safe('arch') not in ['x86', 'x86_64']:
            uimage_source = os.path.join(self.folder, 'arch', self.ARCHITECTURE_MAP[arch], 'boot', 'uImage')
            uimage_destination = os.path.join(self.package_folder, 'boot')
            os.mkdir(uimage_destination)
            shutil.copy2(uimage_source, uimage_destination)

    def configure(self):
        del self.settings.compiler.libcxx
        super(LinuxConan, self).configure()

    def _check_version(self):
        # Ensure we don't have a version mismatch
        p = subprocess.Popen(['make', '-C', self.folder, '--no-print-directory', 'kernelversion'],
                             stdout=subprocess.PIPE)
        stdout = p.communicate()[0]
        make_version = stdout.decode().strip()
        conan_version = self.version.split('+')[0]  # Strip Conan's recipe version
        error_msg = 'Version from build system should match Conan version: Make={0}, Conan={1}' \
            .format(make_version, conan_version)
        assert make_version == conan_version, error_msg

        return make_version

    def _get_make_flags(self):
        flags = ['ARCH={0}'.format(self.ARCHITECTURE_MAP[self.settings.get_safe('arch')])]
        if tools.cross_building(self.settings):
            flags.append('CROSS_COMPILE={0}'.format(os.environ['CC'][:-3]))
        return ' '.join(flags)

    @property
    def relative_folder(self):
        return 'mbl-sw-nt24k-linux-kernel'

    @property
    def folder(self):
        return os.path.join(self.build_folder, self.relative_folder)
