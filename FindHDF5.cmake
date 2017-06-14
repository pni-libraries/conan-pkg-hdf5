set(HDF5_ROOT ${CONAN_HDF5_ROOT})
message(STATUS "******************Conan FindHDF5 wrapper******************")
message(STATUS "Package path: ${CONAN_HDF5_ROOT}")
include(${CONAN_HDF5_ROOT}/FindHDF5_original.cmake)
