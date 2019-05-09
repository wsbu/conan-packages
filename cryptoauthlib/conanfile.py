import os

from conans import ConanFile, CMake


class CryptoAuthLib(ConanFile):
    name = 'cryptoauthlib'
    version = '20190304'
    url = 'https://github.com/wsbu/conan-packages'
    homepage = 'https://github.com/MicrochipTech/cryptoauthlib'
    description = 'Library for interacting with the Crypto Authentication secure elements.'
    settings = 'os', 'compiler', 'build_type', 'arch'
    license = 'MIT'
    options = {
        'shared': [True, False],
        'hal_kit_hid': [True, False],
        'hal_i2c': [True, False],
        'hal_custom': [True, False],
        'printf': [True, False],
        'pkcs11': [True, False],
        'mbedtls': [True, False]
    }
    default_options = {
        'shared': True,
        'hal_kit_hid': False,
        'hal_i2c': False,
        'hal_custom': False,
        'printf': False,
        'pkcs11': False,
        'mbedtls': False
    }

    scm = {
        'type': 'git',
        'url': 'https://github.com/wsbu/cryptoauthlib.git',
        'revision': version
    }

    def configure(self):
        if self.settings.os == 'Linux' and self.options['hal_kit_id']:
            raise Exception("Sorry - libudev isn't generally available in Conan yet so I can't build the library "
                            "with this configuration.")

    def build(self):
        cmake = self.cmake
        cmake.configure(source_folder=os.path.join(self.build_folder, 'lib'), build_folder=self.bin_dir)
        cmake.build()

    def package(self):
        self.copy('*.so' if self.options.shared else '*.a', src=os.path.join(self.bin_dir), dst='lib')
        self.copy('*.h', src=os.path.join(self.build_folder, 'lib'), dst='include')

    def package_info(self):
        self.cpp_info.libs = ['cryptoauth']
        self.cpp_info.includedirs = [
            'include',
            os.path.join('include', 'hal'),
            os.path.join('include', 'basic'),
            os.path.join('include', 'crypto')
        ]

    @property
    def cmake(self):
        cmake = CMake(self)
        cmake.definitions.update({
            'ATCA_HAL_KIT_HID': 'ON' if self.options.hal_kit_hid else 'OFF',
            'ATCA_HAL_I2C': 'ON' if self.options.hal_i2c else 'OFF',
            'ATCA_HAL_CUSTOM': 'ON' if self.options.hal_custom else 'OFF',
            'ATCA_PRINTF': 'ON' if self.options.printf else 'OFF',
            'ATCA_PKCS11': 'ON' if self.options.pkcs11 else 'OFF',
            'ATCA_MBEDTLS': 'ON' if self.options.mbedtls else 'OFF',
            'ATCA_BUILD_SHARED_LIBS': 'ON' if self.options.shared else 'OFF'
        })
        return cmake

    @property
    def bin_dir(self):
        return os.path.join(self.build_folder, 'build')
