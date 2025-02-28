from conan import tools
from conan.tools.files import save, load
import inspect


# A dummy config type to pass to Conan
class _DummyConfig(object):
	def __getattribute__(self, attr):
		return None


class ConanTools(object):
	'''
	Provides access to Conan utility functionality whilst ensuring all required configuration is performed
	'''
	
	# Keep track of whether we have already configured Conan
	_isConanConfigured = False
	
	@staticmethod
	def get(*args, **kwargs):
		'''
		Wraps `conan.tools.get()`
		'''
		ConanTools._configureConan()
		return tools.get(*args, **kwargs)
	
	@staticmethod
	def load(*args, **kwargs):
		'''
		Wraps `conan.tools.files.load()`
		'''
		ConanTools._configureConan()
		return tools.files.load(object, *args, **kwargs)
	
	@staticmethod
	def save(*args, **kwargs):
		'''
		Wraps `conan.tools.save()`
		'''
		ConanTools._configureConan()
		return tools.files.save(object, *args, **kwargs)
	
	@staticmethod
	def _configureConan():
		'''
		Ensures Conan is configured correctly so we can use its utility functionality from outside recipes
		'''
		
		# We only need to perform configuration once
		if ConanTools._isConanConfigured == True:
			return
		
		# Ensure Conan's global configuration object is not `None` when using Conan 1.22.0 or newer
		if hasattr(tools, 'get_global_instances') and hasattr(tools, 'set_global_instances'):
			if 'config' in inspect.signature(tools.set_global_instances).parameters:
				instances = tools.get_global_instances()
				tools.set_global_instances(the_output=instances[0], the_requester=instances[1], config=_DummyConfig())
		
		ConanTools._isConanConfigured = True
