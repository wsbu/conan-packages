cmake_minimum_required(VERSION 3.0)

project(CurlTest C)

include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
conan_basic_setup(TARGETS)

add_executable("${PROJECT_NAME}" "${PROJECT_NAME}.c")
target_link_libraries(${PROJECT_NAME} CONAN_PKG::curl)

enable_testing()
add_test(NAME ${PROJECT_NAME}
    COMMAND ${CMAKE_CROSSCOMPILING_EMULATOR} "$<TARGET_FILE:${PROJECT_NAME}>")
