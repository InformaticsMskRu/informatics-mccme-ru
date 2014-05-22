cmake_minimum_required (VERSION 2.6)
project(Run1C)

find_package(Boost COMPONENTS filesystem system locale REQUIRED)
set(Boost_USE_STATIC_LIBS   ON)
add_definitions(-std=c++1y)
add_executable(Run1C run_code.cpp)
add_library(SoapProxy soapC.cpp soapServiceSoapBindingProxy.cpp)
add_library(stdsoap2 stdsoap2.cpp)

target_link_libraries(Run1C SoapProxy stdsoap2 ${Boost_FILESYSTEM_LIBRARY} ${Boost_SYSTEM_LIBRARY} ${Boost_LOCALE_LIBRARY})
