cmake_minimum_required(VERSION 3.0)

project(LibXml2Test C)

include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
conan_basic_setup(TARGETS)

add_executable("${PROJECT_NAME}" "io1.c")
target_link_libraries(${PROJECT_NAME} CONAN_PKG::libxml2)

enable_testing()
add_test(NAME ${PROJECT_NAME}
    COMMAND $<TARGET_FILE:${PROJECT_NAME}>)
