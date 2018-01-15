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
    options = {
        'shared': [True, False],
        'cxx11': [True, False],
    }
    default_options = 'shared=True', 'cxx11=True'

    ARCHIVE_BASENAME = name.upper() + '_' + version.replace('.', '_')
    FOLDER = name + '-' + ARCHIVE_BASENAME

    def source(self):
        zipname = self.ARCHIVE_BASENAME + '.zip'
        url = 'https://github.com/weidai11/cryptopp/archive/%s' % zipname
        tools.download(url, zipname)
        tools.unzip(zipname)
        os.remove(zipname)

        # Without this, CMake won't know how to find the dependencies that Conan is trying to inject
        tools.replace_in_file(os.path.join(self.FOLDER, 'CMakeLists.txt'), 'project(cryptopp)',
                              '''project(cryptopp)
include("${PROJECT_BINARY_DIR}/conanbuildinfo.cmake")
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.definitions['CMAKE_INSTALL_PREFIX'] = '/'
        cmake.configure(source_dir='cryptopp-CRYPTOPP_5_6_5')
        cmake.build()
        cmake.install(args=['--', 'DESTDIR=' + self.package_folder])

    def package_info(self):
        self.cpp_info.libs = ['cryptopp']
