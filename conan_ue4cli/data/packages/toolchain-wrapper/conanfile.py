from conan import ConanFile
import glob, os, tempfile
from os.path import dirname, join
from conan.tools.files import copy

class ToolchainWrapper(ConanFile):
    name = "toolchain-wrapper"
    version = "ue4"
    author = "Adam Rehn (adam@adamrehn.com)"
    description = "Wraps a clang compiler toolchain, libc++ and a minimal CentOS 7 sysroot"
    url = "https://github.com/adamrehn/conan-ue4cli/tree/master/conan_ue4cli/data/packages/toolchain-wrapper"
    homepage = "https://llvm.org/"
    license = "Apache-2.0"
    settings = "os", "compiler", "arch"
    exports = "*.py"
    
    def _find_clang(self, root, architecture):
        '''
        Attempts to locate the clang binary for the specified architecture under the supplied root directory
        '''
        
        # If we've been pointed directly at a clang toolchain then the binary will be directly under the `bin` subdirectory of the root,
        # whereas if we've been pointed at an Unreal Engine toolchain SDK bundle then there will be per-architecture nested subdirectories
        flat = glob.glob(join(root, "bin", "clang"))
        nested = glob.glob(join(root, "*clang*", "*{}*".format(architecture), "bin", "clang"))
        
        # Determine if we can locate clang
        if len(flat) > 0:
            return flat[0]
        elif len(nested) > 0:
            return nested[0]
        else:
            raise RuntimeError('could not locate clang binary for architecture "{}" inside directory "{}"!'.format(architecture, root))
    
    def _find_libcxx(self, root, architecture):
        '''
        Attempts to locate the libc++ static library for the specified architecture under the supplied root directory
        '''
        folder = "/home/ue4/UnrealEngine/Engine/Source/ThirdParty"
        raise RuntimeError('folder: {} does folder exist: {} folder contents: {}'.format(folder, os.path.isdir(folder), os.listdir(folder)))
        libraries = glob.glob(join(root, "LibCxx","lib", "Linux", "*{}*".format(architecture), "libc++.a"))
        if len(libraries) > 0:
            return libraries[0]

        libraries = glob.glob(join(root, "lib", "Unix", "*{}*".format(architecture), "libc++.a"))
        if len(libraries) > 0:
            return libraries[0]

        raise RuntimeError('Failed to locate libc++.a for architecture "{}" inside directory "{}"!'.format(architecture, join(root, "LibCxx","lib", "Linux", "*{}*".format(architecture), "libc++.a")))
    
    def package(self):
        
        # We currently only support wrapping toolchains targeting Linux
        if self.settings.os != "Linux":
            raise RuntimeError("Only toolchains targeting Linux are supported!")
        
        # We currently only support wrapping toolchains that use clang as the compiler
        if self.settings.compiler != "clang":
            raise RuntimeError("Only toolchains that use clang are supported!")
        
        # Verify that a toolchain path has been supplied for us to wrap
        toolchain = os.environ.get("WRAPPED_TOOLCHAIN", None)
        if toolchain is None:
            raise RuntimeError("Toolchain path must be specified via the WRAPPED_TOOLCHAIN environment variable!")
        
        # Verify that a libc++ path has been supplied for us to wrap
        libcxx = os.environ.get("WRAPPED_LIBCXX", None)
        if libcxx is None:
            raise RuntimeError("libc++ path must be specified via the WRAPPED_LIBCXX environment variable!")
        
        # If we've been pointed to the root SDK directory of an Unreal Engine toolchain, locate the compiler for the target architecture
        architecture = "aarch64" if self.settings.arch == "armv8" else self.settings.arch
        toolchain = dirname(dirname(self._find_clang(toolchain, architecture)))
        
        # Locate the libc++ library files for the target architecture
        libraries = dirname(self._find_libcxx(libcxx, architecture))
        
        # Copy the toolchain files into our package
        print('Copying toolchain files from "{}"...'.format(toolchain))
        copy(self, "*", toolchain, self.package_folder)
        
        # Copy the libc++ header files into our package
        headers = join(libcxx, 'include')
        print('Copying libc++ header files from "{}"...'.format(headers))
        copy(self, "*", headers, join(self.package_folder, "libc++/include"))
        
        # Copy the libc++ library files into our package
        print('Copying libc++ library files from "{}"...'.format(libraries))
        copy(self, "*", libraries, join(self.package_folder, "libc++/lib"))
        
        # Copy our compiler wrapper scripts into the package
        copy(self, "*", self.source_folder, self.package_folder)
        copy(self, "*", self.recipe_folder, self.package_folder)

    def package_info(self):
        
        # Set the relevant environment variables to ensure downstream build systems use our compiler wrapper scripts

        os.environ['CC'] = join(self.package_folder, "wrappers", "clang.py")
        os.environ['CXX'] = join(self.package_folder, "wrappers", "clang++.py")
        os.environ['WRAPPED_CC'] = join(self.package_folder, "bin", "clang")
        os.environ['WRAPPED_CXX'] = join(self.package_folder, "bin", "clang++")
        os.environ['WRAPPED_LIBCXX'] = join(self.package_folder, "libc++")
        os.environ['WRAPPED_SYSROOT'] = self.package_folder
        os.environ['LDFLAGS'] = "---link"
        
        # Ensure our compiler wrapper scripts are executable
        self.run("chmod +x {}/wrappers/clang.py {}/wrappers/clang++.py".format(self.package_folder, self.package_folder))
