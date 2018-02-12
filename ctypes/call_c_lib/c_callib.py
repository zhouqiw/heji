from  ctypes import *
 
libc = CDLL("libSystem.dylib")#mac 的C库 libSystem.dylib，

message_string = "zhouqi,你好"

libc.printf("testing:%s",message_string)
