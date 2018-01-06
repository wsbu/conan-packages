from conans import ConanFile, AutoToolsBuildEnvironment
from conans.tools import download, untargz
import os


class libtoolConan(ConanFile):
    name = 'libtool'
    version = '2.4.6'
    url = 'https://github.com/wsbu/conan-packages'
    license = 'GNU General Public License: https://www.gnu.org/licenses/gpl.html'
    settings = 'os', 'compiler', 'build_type', 'arch'

    FOLDER = 'libtool-' + version
    ARCHIVE = FOLDER + '.tar.gz'

    def source(self):
        download('http://ftpmirror.gnu.org/libtool/' + self.ARCHIVE, self.ARCHIVE)
        untargz(self.ARCHIVE)
        os.remove(self.ARCHIVE)

    def build(self):
        env = AutoToolsBuildEnvironment(self)
        env.configure(configure_dir=self.FOLDER, args=['--prefix=' + self.package_folder])
        env.make()
        env.make(args=['install'])

    def package_info(self):
        self.cpp_info.libs = ['ltdl']
