cmake_minimum_required(VERSION 2.8.4)  #版本最小为2.8.4

PROJECT(Train)   #设置工程名

SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -O2 -DDLIB_JPEG_SUPPORT")

IF(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
  SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Weverything")
ELSEIF(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
  SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra")
ENDIF()



#包含头文件
INCLUDE_DIRECTORIES(/home/whf/dlib-19.16) #dlib根目录地址

LINK_DIRECTORIES(/home/whf/dlib-19.16/build/dlib) #dlib编译后bulid下dlib地址

#生产类似于.exe的可执行文件
ADD_EXECUTABLE(train train.cpp)

TARGET_LINK_LIBRARIES(train dlib)
