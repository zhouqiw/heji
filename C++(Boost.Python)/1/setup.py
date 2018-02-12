from distutils.core import setup
from distutils.extension import Extension

hello_ext = Extension(
    'student',
    sources=['student2py.cpp'],
    libraries=['boost_python-mt'],
)

setup(
    name='student',
    version='0.1',
    ext_modules=[hello_ext])
