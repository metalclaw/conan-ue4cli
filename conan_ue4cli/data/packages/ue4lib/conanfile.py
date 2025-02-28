from conan import ConanFile
from conan.tools.files import copy
import sys, os

class UE4LibConan(ConanFile):
    name = "ue4lib"
    version = "ue4"
    description = """The conan-ue4cli Python package is a 
                    plugin for ue4cli that provides functionality 
                    for generating and using Conan packages that 
                    wrap the third-party libraries bundled in the 
                    Engine/Source/ThirdParty subdirectory of the 
                    Unreal Engine 4 source tree."""
    homepage = "https://github.com/adamrehn/conan-ue4cli"
    author = "Adam Rehn (adam@adamrehn.com)"
    license = "MIT"
    url = "https://github.com/adamrehn/conan-ue4cli/tree/master/conan_ue4cli/data/packages/ue4lib"

    exports = "*.py"
    build_policy = "missing"
    
    def package(self):
        copy(self, "*.py", self.build_folder, self.package_folder)
        copy(self, "*.py", self.source_folder, self.package_folder)
        copy(self, "*.py", self.recipe_folder, self.package_folder)

    def package_info(self):
        os.environ['PATH'] += ':' + self.package_folder
        if os.getenv("PYTHONPATH") is not None:
            os.environ['PYTHONPATH'] += self.package_folder
        else:
            os.environ['PYTHONPATH'] = self.package_folder
