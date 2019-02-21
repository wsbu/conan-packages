cmake_minimum_required(VERSION 3.0)

project(GooletestTest)

include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
conan_basic_setup(TARGETS)

find_package(GTest REQUIRED
    PATHS "${CONAN_GOOGLETEST_ROOT}")

enable_testing()

add_executable(${PROJECT_NAME}_gtest            "${PROJECT_NAME}_gtest.cpp")
target_link_libraries(${PROJECT_NAME}_gtest     GTest::gtest_main)
add_test(NAME ${PROJECT_NAME}_gtest
    COMMAND ${CMAKE_CROSSCOMPILING_EMULATOR} "$<TARGET_FILE:${PROJECT_NAME}_gtest>")

add_test(NAME ${PROJECT_NAME}_gmock
    COMMAND ${CMAKE_CROSSCOMPILING_EMULATOR} "$<TARGET_FILE:${PROJECT_NAME}_gmock>")
add_executable(${PROJECT_NAME}_gmock            "${PROJECT_NAME}_gmock.cpp")
target_link_libraries(${PROJECT_NAME}_gmock     GTest::gmock_main)
