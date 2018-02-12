#!/usr/bin/env python

import example
import timeit

print example.fact(3)

t = timeit.timeit('example.sum(100)',setup="from __main__ import example",number=1)
print t
print example.sum1(20)
#print example.sum(2)
#print example.sum(3)

