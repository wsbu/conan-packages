cmake_minimum_required(VERSION 2.8)

project(ZeroMQTest)

find_package(libzmq REQUIRED)

add_executable(ZeroMQ_test ZeroMQTest.cpp)
target_link_libraries(ZeroMQ_test libzmq::libzmq)

enable_testing()
add_test(NAME ZeroMQ_test
    COMMAND ${CMAKE_CROSSCOMPILING_EMULATOR} "$<TARGET_FILE:ZeroMQ_test>")
