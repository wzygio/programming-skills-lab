import ctypes
from timeit import default_timer as timer

# load the shared object file 
cpp = ctypes.cdll.LoadLibrary('.\\percolate.dll')
percolate = cpp.main

# transform data type
para = "-l30"
para = bytes(para,encoding = "utf8")
print(type(para),str(para))
para = ctypes.c_char_p(para)
print(type(para),str(para))

tic = timer()
percolate(2,para)
toc = timer()

print("Runtime: "+str(toc - tic)) # 输出的时间，秒为单位



"""
import ctypes
 
#load the shared object file
adder = ctypes.cdll.LoadLibrary('.\\adder.dll')
 
#Find sum of integers
res_int = adder.add_int(4,5)
print("4 + 5 = " + str(res_int))
 
#Find sum of floats
a = ctypes.c_float(5.5)
b = ctypes.c_float(4.1)

# no need for transform the function's data type 
add_float = adder.add_float
add_float.restype = ctypes.c_float
 
print("5.5 + 4.1 = " + str(add_float(a, b)))
"""

