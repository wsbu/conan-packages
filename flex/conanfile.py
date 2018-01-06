from conans import ConanFile, AutoToolsBuildEnvironment
from conans.tools import download, untargz
import os


class FlexConan(ConanFile):
    name = 'flex'
    version = '2.6.3'
    url = 'https://github.com/wsbu/conan-packages'
    license = 'GNU General Public License: https://www.gnu.org/licenses/gpl.html'
    settings = 'os', 'compiler', 'build_type', 'arch'

    requires = "bison/3.0.4@wsbu/testing"

    FOLDER = 'flex-' + version
    ARCHIVE = FOLDER + '.tar.gz'

    def source(self):
        download('https://github.com/westes/flex/releases/download/v%s/%s' % (self.version, self.ARCHIVE), self.ARCHIVE)
        untargz(self.ARCHIVE)
        os.remove(self.ARCHIVE)

    def build(self):
        env = AutoToolsBuildEnvironment(self)

        os.environ['PATH'] += os.pathsep + os.pathsep.join(self.deps_cpp_info.bindirs)
        env.configure(configure_dir=self.FOLDER, args=['--prefix=' + self.package_folder])
        env.make()
        env.make(args=['install'])

    def package_info(self):
        # Don't list the libraries generated; flex is mainly used as a tool
        self.cpp_info.resdirs = ['share/flex']
