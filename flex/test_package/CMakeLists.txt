cmake_minimum_required(VERSION 2.8.12)

project(TestFlex)

include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
conan_basic_setup()

find_package(FLEX)

# Add a test grammar
flex_target(test-flex basic_nr.l "${CMAKE_CURRENT_BINARY_DIR}/basic_nr.c")
message(STATUS "Flex executable: ${FLEX_EXECUTABLE}")

add_executable(test-flex ${FLEX_test-flex_OUTPUTS})
target_include_directories(test-flex PUBLIC
        "${CMAKE_CURRENT_BINARY_DIR}"
        "${CMAKE_CURRENT_SOURCE_DIR}")
target_link_libraries(test-flex m)
