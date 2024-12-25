from conan import ConanFile, tools
from conan.tools.files import copy

class LibCxxConan(ConanFile):
    name = "libcxx"
    version = "ue4"
    homepage = "https://github.com/adamrehn/conan-ue4cli"
    author = "Adam Rehn (adam@adamrehn.com)"
    license = "MIT"
    url = "https://github.com/adamrehn/conan-ue4cli/tree/master/conan_ue4cli/data/packages/libcxx"

    exports = "*.py"
    build_policy = "missing"
    
    def package(self):
        copy(self, "*.py", self.source_folder, self.package_folder)
    
    def package_info(self):
        
        # Provide the libcxx Python module for backwards compatibility with recipes written for older versions of conan-ue4cli
        self.env_info.PYTHONPATH.append(self.package_folder)
