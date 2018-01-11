cmake_minimum_required(VERSION 3.0)

project(cryptoppTest)

include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
conan_basic_setup()

find_package(cryptopp REQUIRED)

add_executable("${PROJECT_NAME}" "${PROJECT_NAME}.cpp")
target_link_libraries(${PROJECT_NAME} cryptopp)

enable_testing()
add_test(NAME ${PROJECT_NAME}
    COMMAND ${CMAKE_CROSSCOMPILING_EMULATOR} "$<TARGET_FILE:${PROJECT_NAME}>")
