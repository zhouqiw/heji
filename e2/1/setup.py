#!/usr/bin/env python  
  
from distutils.core import setup, Extension  
  
MOD = 'testm'
setup(name=MOD, ext_modules=[Extension(MOD, sources=['testm.c'])]), 
