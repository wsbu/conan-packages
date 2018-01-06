cmake_minimum_required(VERSION 2.8.12)

project(TestBison)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

find_package(BISON)

# Add a test grammar
bison_target(test-bison mfcalc.y "${CMAKE_CURRENT_BINARY_DIR}/mfcalc.c" VERBOSE "${CMAKE_CURRENT_BINARY_DIR}/mfcalc.output")
message(STATUS "Bison executable: ${BISON_EXECUTABLE}")

add_executable(test-bison ${BISON_test-bison_OUTPUTS})
target_include_directories(test-bison PUBLIC
        "${CMAKE_CURRENT_BINARY_DIR}"
        "${CMAKE_CURRENT_SOURCE_DIR}")
target_link_libraries(test-bison m)
