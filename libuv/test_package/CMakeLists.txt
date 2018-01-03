cmake_minimum_required(VERSION 3.0)

project(LibUVTest C)

include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
conan_basic_setup(TARGETS)

add_executable("${PROJECT_NAME}" "${PROJECT_NAME}.c")
target_link_libraries(${PROJECT_NAME} CONAN_PKG::libuv)

enable_testing()
add_test(NAME ${PROJECT_NAME}
    COMMAND $<TARGET_FILE:${PROJECT_NAME}>)
