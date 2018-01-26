cmake_minimum_required(VERSION 2.8)

project(OpenSSLTest)

include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
conan_basic_setup()

find_package(OpenSSL REQUIRED)

add_executable(md5 md5.cpp)
target_link_libraries(md5 OpenSSL::SSL)

enable_testing()
add_test(NAME md5
    COMMAND ${CMAKE_CROSSCOMPILING_EMULATOR} "$<TARGET_FILE:md5>")
