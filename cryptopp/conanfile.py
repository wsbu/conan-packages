from conans import ConanFile, CMake
from conans import tools
import os


class CryptoPPConan(ConanFile):
    name = 'cryptopp'
    version = '5.6.5-1'
    cryptopp_version = version.split('-')[0]
    url = 'https://github.com/wsbu/conan-packages'
    description = 'Crypto++ Library is a free C++ class library of cryptographic schemes.'
    settings = 'os', 'compiler', 'build_type', 'arch'
    license = 'Boost Software License 1.0'
    generators = 'cmake'
    options = {
        'cxx11': [True, False],
    }
    default_options = 'cxx11=True'

    ARCHIVE_BASENAME = name.upper() + '_' + cryptopp_version.replace('.', '_')
    FOLDER = name + '-' + ARCHIVE_BASENAME

    def source(self):
        zipname = self.ARCHIVE_BASENAME + '.zip'
        url = 'https://github.com/weidai11/cryptopp/archive/%s' % zipname
        tools.download(url, zipname)
        tools.unzip(zipname)
        os.remove(zipname)

    def build(self):
        source_dir = os.path.join(self.build_folder, self.FOLDER)
        build_dir = os.path.join(self.build_folder, 'build')

        # Without this, CMake won't know how to find the dependencies that Conan is trying to inject
        # Also, set the `conan_output_dirs_setup()` macro to empty or else unit tests will fail
        tools.replace_in_file(os.path.join(source_dir, 'CMakeLists.txt'), 'project(cryptopp)',
                              '''project(cryptopp)
include("{0}/conanbuildinfo.cmake")
conan_basic_setup()'''.format(self.build_folder))

        cmake = CMake(self)
        cmake.configure(source_dir=source_dir, build_dir=build_dir)
        cmake.build()

    def package(self):
        self.run('cmake --build {0} --target install'.format(os.path.join(self.build_folder, 'build')))

    def package_info(self):
        self.cpp_info.libs = ['cryptopp']
