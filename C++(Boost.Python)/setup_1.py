from distutils.core import setup
from distutils.extension import Extension

hello_world = Extension(
    'hello_world',
    sources=['hello_world.cpp'],
    libraries=['boost_python-mt'],
)

setup(
    name='hello-world_0',
    version='0.1',
    ext_modules=[hello_world])
