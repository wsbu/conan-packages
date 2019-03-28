cmake_minimum_required(VERSION 2.8)

project(ZeroMQTest)

include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
conan_basic_setup(TARGETS)

find_package(ZeroMQ REQUIRED)

add_executable(ZeroMQ_test ZeroMQTest.cpp)
target_link_libraries(ZeroMQ_test libzmq)

enable_testing()
add_test(NAME ZeroMQ_test
    COMMAND ${CMAKE_CROSSCOMPILING_EMULATOR} "$<TARGET_FILE:ZeroMQ_test>")
