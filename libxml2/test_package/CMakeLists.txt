cmake_minimum_required(VERSION 3.0)

project(LibXml2Test C)

include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
conan_basic_setup()

find_package(LibXml2 REQUIRED)

add_executable("${PROJECT_NAME}" "io1.c")
target_link_libraries(${PROJECT_NAME} ${LIBXML2_LIBRARIES})
target_include_directories(${PROJECT_NAME} PRIVATE ${LIBXML2_INCLUDE_DIR})

enable_testing()
add_test(NAME ${PROJECT_NAME}
    COMMAND ${CMAKE_CROSSCOMPILING_EMULATOR} "$<TARGET_FILE:${PROJECT_NAME}>")
