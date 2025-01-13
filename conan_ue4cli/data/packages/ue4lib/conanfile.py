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
        print(os.listdir(self.source_folder))
        raise Exception("the hell?")

    def package_info(self):
        self.runenv_info.prepend_path("PYTHONPATH", self.package_folder)
        self.runenv_info.prepend_path("PATH", self.package_folder)
        self.buildenv_info.prepend_path("PYTHONPATH", self.package_folder)
        self.buildenv_info.prepend_path("PATH", self.package_folder)
        self.runenv.prepend_path("PYTHONPATH", self.package_folder)
        self.runenv.prepend_path("PATH", self.package_folder)
        self.buildenv.prepend_path("PYTHONPATH", self.package_folder)
        self.buildenv.prepend_path("PATH", self.package_folder)
        self.run("export PYTHONPATH=" + self.package_folder)
        sys.path.append(self.package_folder)
        os.environ['PATH'] += ':' + self.package_folder
        os.environ['PYTHONPATH'] = self.package_folder
