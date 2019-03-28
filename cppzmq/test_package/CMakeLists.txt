cmake_minimum_required(VERSION 2.8)

project(CppZmqTest)
include("${PROJECT_BINARY_DIR}/conanbuildinfo.cmake")
conan_basic_setup(TARGETS)

find_package(ZeroMQ REQUIRED)
find_package(cppzmq REQUIRED)

add_executable(CppZmq_test CppZmqTest.cpp)
target_link_libraries(CppZmq_test cppzmq)

enable_testing()
add_test(NAME CppZmq_test
    COMMAND ${CMAKE_CROSSCOMPILING_EMULATOR} "$<TARGET_FILE:CppZmq_test>")
