cmake_minimum_required(VERSION 2.8)

project(TinyXMLTest)

find_package(tinyxml REQUIRED)

add_executable(tinyxml_test main.cpp)
target_compile_options(tinyxml_test PRIVATE -w)
target_link_libraries(tinyxml_test tinyxml::tinyxml)

enable_testing()
add_test(NAME tinyxml_test
    COMMAND ${CMAKE_CROSSCOMPILING_EMULATOR} "$<TARGET_FILE:tinyxml_test>"
    WORKING_DIRECTORY "${CMAKE_CURRENT_LIST_DIR}")
