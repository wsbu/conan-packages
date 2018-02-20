cmake_minimum_required(VERSION 3.0)

project(libpoptTest C)

include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
conan_basic_setup(TARGETS)

find_library(POPT_LIB popt)
find_path(POPT_INCLUDE_DIR popt.h)

if (NOT POPT_LIB)
    message(FATAL_ERROR "Unable to find libpopt")
endif ()
if (NOT POPT_INCLUDE_DIR)
    message(FATAL_ERROR "Unable to find libpopt's header file.")
endif ()

add_executable("${PROJECT_NAME}" "${PROJECT_NAME}.c")
target_link_libraries(${PROJECT_NAME} "${POPT_LIB}")
target_include_directories(${PROJECT_NAME} PRIVATE "${POPT_INCLUDE_DIR}")

enable_testing()
add_test(NAME ${PROJECT_NAME}
    COMMAND ${CMAKE_CROSSCOMPILING_EMULATOR} "$<TARGET_FILE:${PROJECT_NAME}>" -a 123 -b 456 -c 789)
