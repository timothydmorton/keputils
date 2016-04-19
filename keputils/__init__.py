__version__ = '0.2'

try:
    __KEPUTILS_SETUP__
except NameError:
    __KEPUTILS_SETUP__ = False

if not __KEPUTILS_SETUP__:
	__all__ = ['koiutils','kicutils']
