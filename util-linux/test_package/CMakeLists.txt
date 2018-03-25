cmake_minimum_required(VERSION 3.0)

project(UtilLinuxTest C)

include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
conan_basic_setup()

find_path(UUID_HEADER "uuid/uuid.h")
find_library(LIB_UUID "uuid")

add_executable("${PROJECT_NAME}" "${PROJECT_NAME}.c")
target_include_directories("${PROJECT_NAME}" PRIVATE "${UUID_HEADER}")
target_link_libraries(${PROJECT_NAME} PUBLIC "${LIB_UUID}")

enable_testing()
add_test(NAME ${PROJECT_NAME}
    COMMAND ${CMAKE_CROSSCOMPILING_EMULATOR} "$<TARGET_FILE:${PROJECT_NAME}>")
