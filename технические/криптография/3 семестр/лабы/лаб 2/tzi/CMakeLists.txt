cmake_minimum_required(VERSION 2.8) 
project(TZICryptDynamic)

set(SOURCES main.cpp)

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)
link_directories(${CMAKE_CURRENT_SOURCE_DIR}/libs)

add_executable(TZICryptDynamic ${SOURCES})

target_link_libraries(TZICryptDynamic PRIVATE TZICrypt)