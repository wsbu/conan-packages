from conans import ConanFile, AutoToolsBuildEnvironment
from conans.tools import download, untargz
import os


class BisonConan(ConanFile):
    name = 'bison'
    version = '3.0.4'
    url = 'https://github.com/wsbu/conan-packages'
    license = 'GNU General Public License: https://www.gnu.org/licenses/gpl.html'
    settings = 'os', 'compiler', 'build_type', 'arch'

    FOLDER = 'bison-' + version
    ARCHIVE = FOLDER + '.tar.gz'

    def source(self):
        download('http://ftp.gnu.org/gnu/bison/' + self.ARCHIVE, self.ARCHIVE)
        untargz(self.ARCHIVE)
        os.remove(self.ARCHIVE)

    def build(self):
        env = AutoToolsBuildEnvironment(self)
        env.configure(configure_dir=self.FOLDER, args=['--prefix=' + self.package_folder])
        env.make()
        env.make(args=['install'])

    def package_info(self):
        # Don't list the libraries generated; bison is mainly used as a tool
        self.cpp_info.resdirs = ['share/bison']
