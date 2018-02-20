from conans import ConanFile, CMake, tools


class LibpoptTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if tools.cross_building(self.settings):
            self.output.info('This test always fails when cross-compiling. Skipping test.')
        else:
            self.run('ctest --output-on-failure')

    def configure(self):
        del self.settings.compiler.libcxx
        super(LibpoptTestConan, self).configure()
