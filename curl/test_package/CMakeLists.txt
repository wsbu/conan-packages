cmake_minimum_required(VERSION 3.0)

project(CurlTest C)

include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
conan_basic_setup(TARGETS)

find_package(CURL REQUIRED)

add_executable("${PROJECT_NAME}" "${PROJECT_NAME}.c")
target_link_libraries(${PROJECT_NAME} ${CURL_LIBRARIES})
target_include_directories(${PROJECT_NAME} PRIVATE ${CURL_INCLUDE_DIR})

enable_testing()
add_test(NAME ${PROJECT_NAME}
    COMMAND ${CMAKE_CROSSCOMPILING_EMULATOR} "$<TARGET_FILE:${PROJECT_NAME}>")
