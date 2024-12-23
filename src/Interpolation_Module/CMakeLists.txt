cmake_minimum_required(VERSION 3.10)
project(Interpolation_Module)

# Set the module
set(MODULE Interpolation_Module)

# Compilation Flags
set(CXXFLAGS "-Wall -Wextra -Wpedantic -Werror -Wno-nested-anon-types -g -fPIC")

# Find GSL
find_package(GSL REQUIRED)
if (NOT GSL_FOUND)
    message(FATAL_ERROR "GSL not found!")
endif()

# Set relative paths
set(ROOT_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../..)
set(SRC_DIR ${ROOT_DIR}/src)
set(INCLUDE_DIR ${ROOT_DIR}/include)
set(MODULE_INCLUDE_DIR ${INCLUDE_DIR}/${MODULE})
set(MODULE_SRC_DIR ${SRC_DIR}/${MODULE})
set(MAIN_DIR ${ROOT_DIR}/main)
set(TEST_DIR ${ROOT_DIR}/tests)
set(LIB_DIR ${ROOT_DIR}/lib)
set(BIN_DIR ${ROOT_DIR}/bin)

# Set the include directories
include_directories(
    ${INCLUDE_DIR}
    ${MODULE_INCLUDE_DIR}
)

# Set the source files for the module
file(GLOB_RECURSE MODULE_SOURCES ${MODULE_SRC_DIR}/*.cpp)

# Create the DYNAMIC library
add_library(${MODULE} SHARED ${MODULE_SOURCES})

# Link the module with GSL
target_link_libraries(${MODULE} GSL::gsl)

# Set the output directory for the library
set_target_properties(${MODULE} PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${LIB_DIR})

# Create executable for the main program
add_executable(main_interpolation ${MAIN_DIR}/Interpolation_Module_main.cpp)

# Link the main program with the module
target_link_libraries(main_interpolation ${MODULE})

# Create executable for testing
add_executable(test_interpolation ${TEST_DIR}/Interpolation_Module_test.cpp)

# Link the test program with the module
target_link_libraries(test_interpolation ${MODULE})

# Specify include directories for the test and main programs
target_include_directories(main_interpolation PUBLIC ${INCLUDE_DIR} ${MODULE_INCLUDE_DIR})
target_include_directories(test_interpolation PUBLIC ${INCLUDE_DIR} ${MODULE_INCLUDE_DIR})

# Set the output directory for executables at runtime (main and test)
set_target_properties(main_interpolation test_interpolation PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${BIN_DIR})

# Custom target for running the main program
add_custom_target(run-interpolation
    COMMAND ${BIN_DIR}/main_interpolation
    DEPENDS main_interpolation
    WORKING_DIRECTORY ${BIN_DIR}
)

# Custom target for running the test program
add_custom_target(test-interpolation
    COMMAND ${BIN_DIR}/test_interpolation
    DEPENDS test_interpolation
    WORKING_DIRECTORY ${BIN_DIR}
)
