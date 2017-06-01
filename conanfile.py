from conans import ConanFile, CMake, tools
import os
from conans.tools import untargz
import os.path


class Hdf5Conan(ConanFile):
    name = "hdf5"
    version = "1.10.1"
    license = "<Put the package license here>"
    #url = "https://www.hdfgroup.org/downloads/hdf5/source-code/"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
                "with_tests":[True,False]}
    default_options = "shared=True","with_tests=False"
    requires="zlib/1.2.8@lasote/stable"
    generators = "cmake"
    exports_sources="*.tar.gz"

    def source(self):
        archive_file = "hdf5-1.10.1.tar.gz"
        tools.unzip(archive_file)
        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
        tools.replace_in_file("hdf5-1.10.1/CMakeLists.txt", "PROJECT (HDF5 C CXX)",
        '''PROJECT(HDF5 C CXX)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def configure(self):

        self.options["zlib"].shared = self.options.shared

    def build(self):
        self.source_dir = os.path.join(self.conanfile_directory,"hdf5-1.10.1")
        self.build_dir = os.path.join(self.conanfile_directory,"build")
        self.install_dir = os.path.join(self.conanfile_directory,"install")


        cmake = CMake(self)
        cmake_defs = {}

        if self.options["shared"]:
            cmake_defs["BUILD_SHARED_LIBS"] = "ON"

        cmake_defs["HDF5_BUILD_EXAMPLES"] = "OFF"
        cmake_defs["HDF5_BUILD_TOOLS"]="OFF"
        cmake_defs["HDF5_BUILD_HL_LIB"]="OFF"
        cmake_defs["HDF5_BUILD_CPP_LIB"]="OFF"
        cmake_defs["HDF5_ENABLE_Z_LIB_SUPPORT"]="ON"
        cmake_defs["CMAKE_INSTALL_PREFIX"]=self.package_folder

        cmake.configure(source_dir = "hdf5-1.10.1",
                        defs = cmake_defs,
                        )

        cmake.build()

        # we to not want to run the tests all the time
        if self.options.with_tests:
            if self.settings.os=="Windows":
                cmake.build(target="RUN_TESTS")
            else:
                cmake.build(target="test")

        #finally we call the install target which should greatly simplify the
        #installation process in the package method
        cmake.build(target="install")

    def package(self):
        pass

    def package_info(self):
        self.cpp_info.libs = ["hdf5"]

    def imports(self):
        #if on windows we have to import the zlib.dll to make the
        #tests run
        if self.settings.os=="Windows":
            self.copy("*.dll","bin","bin")
