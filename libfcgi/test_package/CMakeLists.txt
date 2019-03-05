cmake_minimum_required(VERSION 3.3)

project(libfcgiTest)

find_package(libfcgi REQUIRED)

add_executable(fcgi_test main.cpp)
target_link_libraries(fcgi_test libfcgi::libfcgi)

enable_testing()
add_test(NAME fcgi_test
    COMMAND ${CMAKE_CROSSCOMPILING_EMULATOR} "$<TARGET_FILE:fcgi_test>")
