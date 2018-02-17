from ctypes import *
from time import time


def fuction():
    ts = time()
    msvcrt = CDLL("libSystem.dylib")
    for i in xrange(2000000):
    
        message_string = "hello ctypes!\n"
        msvcrt.printf("testing:%s",message_string)

    print time()- ts

def fuction_0():
    ts = time()
    for i in xrange(2000000):
        message_string = "hello ctypes!\n"
        print "testing:%s",message_string
    return time()- ts
def demo():
    
    so = cdll.LoadLibrary
    lib = so("./libpycallclass.so")
    print 'display()'
    ts = time()
    lib.display()
    return time()- ts
    print 'display(100)'
    lib.display_int(100)
#fuction()
t1 =fuction_0()
t2 = demo()

print 't1=%f'%(t1)
print 't2=%f'%(t2)
