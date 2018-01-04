from conans import ConanFile, CMake
from conans import tools
import os


class CryptoPPConan(ConanFile):
    name = 'cryptopp'
    version = '5.6.5'
    url = 'https://github.com/wsbu/conan-packages'
    description = 'Crypto++ Library is a free C++ class library of cryptographic schemes.'
    settings = 'os', 'compiler', 'build_type', 'arch'
    license = 'Boost Software License 1.0'
    generators = 'cmake'
    options = {'shared': [True, False]}
    default_options = 'shared=True'

    def source(self):
        zipname = 'CRYPTOPP_5_6_5.zip'
        url = 'https://github.com/weidai11/cryptopp/archive/%s' % zipname
        sha256 = 'c934d2c427a0ef197ea989a00f7b6d866d110dd55257d2944d0513b382b7e2b4'
        tools.download(url, zipname)
        tools.check_sha256(zipname, sha256)
        tools.unzip(zipname)
        os.remove(zipname)

        # Without this, CMake won't know how to find the dependencies that Conan is trying to inject
        tools.replace_in_file('cryptopp-CRYPTOPP_5_6_5/CMakeLists.txt', 'project(cryptopp)',
                              '''project(cryptopp)
include("${PROJECT_BINARY_DIR}/conanbuildinfo.cmake")
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_dir='cryptopp-CRYPTOPP_5_6_5')
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ['cryptopp']
