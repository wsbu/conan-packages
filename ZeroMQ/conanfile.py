import os

from conans import ConanFile, CMake


class ZeroMQ(ConanFile):
    name = 'ZeroMQ'
    version = '4.2.0'
    url = 'https://github.com/wsbu/conan-packages'
    description = 'Open Source C++ OPC-UA Server and Client Library'
    settings = 'os', 'compiler', 'build_type', 'arch'
    license = 'LGPL-3.0'
    options = {
        'enable_curve': [True, False],
        'enable_drafts': [True, False],
        'enable_eventfd': [True, False],
        'poller': ['kqueue', 'epoll', 'devpoll', 'pollset', 'poll', 'select', 'autodetect'],
        'with_sodium': [True, False],
        'with_militant': [True, False],
        'with_openpgm': [True, False],
        'with_perf_tool': [True, False],
        'with_vmci': [True, False],
        'zmq_build_tests': [True, False]
    }
    default_options = (
        'enable_curve=True',
        'enable_drafts=True',
        'enable_eventfd=False',
        'poller=autodetect',
        'with_sodium=False',
        'with_militant=False',
        'with_openpgm=False',
        'with_perf_tool=True',
        'with_vmci=False',
        'zmq_build_tests=True'
    )

    generators = 'cmake'

    scm = {
        'type': 'git',
        'url': 'git@bitbucket.org:redlionstl/zeromq.git',
        'revision': 'v' + version
    }

    def build(self):
        cmake = self.cmake
        cmake.build()
        if self.options.zmq_build_tests:
            cmake.parallel = False
            cmake.test()

    def package(self):
        self.cmake.install()

    def package_info(self):
        self.cpp_info.libs = [
            'zmq', 'zmq-static'
        ]

    @property
    def cmake(self):
        definitions = {
            'ENABLE_CURVE': 'ON' if self.options.enable_curve else 'OFF',
            'ENABLE_DRAFTS': 'ON' if self.options.enable_drafts else 'OFF',
            'ENABLE_EVENTFD': 'ON' if self.options.enable_eventfd else 'OFF',
            'WITH_SODIUM': 'ON' if self.options.with_sodium else 'OFF',
            'WITH_MILITANT': 'ON' if self.options.with_militant else 'OFF',
            'WITH_OPENPGM': 'ON' if self.options.with_openpgm else 'OFF',
            'WITH_PERF_TOOL': 'ON' if self.options.with_perf_tool else 'OFF',
            'WITH_VMCI': 'ON' if self.options.with_vmci else 'OFF',
            'ZMQ_BUILD_TESTS': 'ON' if self.options.zmq_build_tests else 'OFF'
        }
        if self.options.poller != 'autodetect':
            definitions['POLLER'] = self.options.poller

        cmake = CMake(self)
        cmake.configure(defs=definitions, source_folder=self.build_folder,
                        build_folder=os.path.join(self.build_folder, 'build'))
        return cmake
