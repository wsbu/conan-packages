from conans import ConanFile, CMake


class UtilLinuxTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        self.run('ctest --output-on-failure')

    def configure(self):
        del self.settings.compiler.libcxx
        super(UtilLinuxTestConan, self).configure()
