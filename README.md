sudo pip install -U wxpy -i https://pypi.doubanio.com/simple/



Suppose that you defined a SWIG module such as the following:
创建识别文件example.i
/* File: example.i */ 
%module example  
%{
 #define SWIG_FILE_WITH_INIT #include "example.h" %} 
 int fact(int n); 

 	创建要调用的c文件：
/* File: example.c */ 
 #include "example.h" 
 int fact(int n) 
{   
  if (n < 0)
	{ /* This should probably return an error, but this is simpler */
         return 0;     }    
 if (n == 0) {       
  	return 1;     }    
 else {       
  /* testing for overflow would be a good idea here */       
  	return n * fact(n-1);   
  } 
}
创建头文件example.h
/* File: example.h */ 
 int fact(int n);





Here is a sample setup.py file for the above example:

#!/usr/bin/env python  
""" setup.py file for SWIG example """  
from distutils.core import setup, Extension   
example_module=Extension('_example',                       sources=['example_wrap.c', 'example.c'], )  
setup (name = 'example',        version = '0.1',        author      = "SWIG Docs",        description = """Simple swig example from docs""",        
ext_modules = [example_module],        py_modules = ["example"],        )

执行的命令行：

$ swig -python example.i 
$ python setup.py build_ext --inplace

result ：
Type "help", "copyright", "credits" or "license" for more information.
>>> import example
>>> example.facet(8)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'module' object has no attribute 'facet'
>>> example.fact(8)
40320
>>> example.fact(0)
1
>>> example.fact(-9)
0
>>>







使用Python的ctypes，我们可以直接调用由C直接编译出来的函数。其实就是调用动态链接库中的函数。为什么我们需要这样做呢，因为有些时候，我们可能需要一个性能上比较讲究的算法，有些时候，我们可以在Python中使用已经有了的现成的被封闭在动态链接库中的函数。下面是如何调用的示例。
首先，我们用一个乘法来表示一个算法功能。下面是C的程序：
1
2
3
4
5	int
multiply(int num1, int num2)
{
    return num1 * num2;
}
如果在Windows下，你可能需要写成下面这个样子：
1
2
3
4
5
6
7
8
9
10
11
12
13
14	#include <windows.h>
 
 
BOOL APIENTRY
DllMain(HANDLE hModule, DWORD dwReason, LPVOID lpReserved)
{
    return TRUE;
}
 
__declspec(dllexport) int
multiply(int num1, int num2)
{
    return num1 * num2;
}
然后，自然是把这个C文件编成动态链接库：
Linux下的编译：
1
2	gcc -c -fPIC libtest.c
gcc -shared libtest.o -o libtest.so
Windows下的编译：
1	cl -LD libtest.c -libtest.dll
于是在我们的Python中可以这样使用：
(其中的libtest.so在Windows下改成libtest.dll即可)
1
2
3
4
5	>>> from ctypes import *
>>> import os
>>> libtest = cdll.LoadLibrary(os.getcwd() + '/libtest.so')
>>> print libtest.multiply(2, 2)
4
注意：上面的Python脚本中需要把动态链接库放到当前目录中
>>> from ctypes import *
>>> msvcrt = CDLL("libSystem.dylib")
>>> message_string = "hello ctypes!\n"
>>> msvcrt.printf("testing:%s",message_string)
testing:hello ctypes!
22
>>> msvcrt.printf("testing:%s",message_string)
testing:hello ctypes!
22
>>> msvcrt.printf("testing:%s",message_string)
testing:hello ctypes!
22
>>> msvcrt.printf("testing:%s",message_string)
testing:hello ctypes!
22
>>> n = msvcrt.printf("testing:%s",message_string)
testing:hello ctypes!
>>> n


















Python是解释性语言, 底层就是用c实现的, 所以用python调用C是很容易的, 下面就总结一下各种调用的方法, 给出例子, 所有例子都在ubuntu9.10, python2.6下试过.
 
1. Python 调用 C (base)
想在python中调用c函数, 如这儿的fact
#include <Python.h>

int fact(int n)
{
  if (n <= 1)
    return 1;
  else
    return n * fact(n - 1);
}

PyObject* wrap_fact(PyObject* self, PyObject* args)
{
  int n, result;

  if (! PyArg_ParseTuple(args, "i:fact", &n))
    return NULL;
  result = fact(n);
  return Py_BuildValue("i", result);
}

static PyMethodDef exampleMethods[] =
{
  {"fact", wrap_fact, METH_VARARGS, "Caculate N!"},
  {NULL, NULL}
};

void initexample()
{
  PyObject* m;
  m = Py_InitModule("example", exampleMethods);
}
 
把这段代码存为wrapper.c, 编成so库,
gcc -fPIC wrapper.c -o example.so -shared  -I/usr/include/python2.6 -I/usr/lib/python2.6/config
 
然后在有此so库的目录, 进入python, 可以如下使用
import example
example.fact(4)
 
2. Python 调用 C++ (base)
在python中调用C++类成员函数, 如下调用TestFact类中的fact函数,
#include <Python.h>

class TestFact{
    public:
    TestFact(){};
    ~TestFact(){};
    int fact(int n);
};

int TestFact::fact(int n)
{
  if (n <= 1)
    return 1;
  else
    return n * (n - 1);
}

int fact(int n)
{
    TestFact t;
    return t.fact(n);
}
PyObject* wrap_fact(PyObject* self, PyObject* args)
{
  int n, result;

  if (! PyArg_ParseTuple(args, "i:fact", &n))
    return NULL;
  result = fact(n);
  return Py_BuildValue("i", result);
}

static PyMethodDef exampleMethods[] =
{
  {"fact", wrap_fact, METH_VARARGS, "Caculate N!"},
  {NULL, NULL}
};

extern "C"              //不加会导致找不到initexample
void initexample()
{
  PyObject* m;
  m = Py_InitModule("example", exampleMethods);
}
 
把这段代码存为wrapper.cpp, 编成so库,
g++ -fPIC wrapper.cpp -o example.so -shared -I/usr/include/python2.6 -I/usr/lib/python2.6/config
 
然后在有此so库的目录, 进入python, 可以如下使用
import example
example.fact(4)
 
3. Python 调用 C++ (Boost.Python)
Boost库是非常强大的库, 其中的python库可以用来封装c++被python调用, 功能比较强大, 不但可以封装函数还能封装类, 类成员.
http://dev.gameres.com/Program/Abstract/Building%20Hybrid%20Systems%20with%20Boost_Python.CHN.by.JERRY.htm
首先在ubuntu下安装boost.python, apt-get install libboost-python-dev
#include <boost/python.hpp>
char const* greet()
{
   return "hello, world";
}

BOOST_PYTHON_MODULE(hello)
{
    using namespace boost::python;
    def("greet", greet);
}
把代码存为hello.cpp, 编译成so库
g++ hello.cpp -o hello.so -shared -I/usr/include/python2.5 -I/usr/lib/python2.5/config -lboost_python-gcc42-mt-1_34_1
 
此处python路径设为你的python路径, 并且必须加-lboost_python-gcc42-mt-1_34_1, 这个库名不一定是这个, 去/user/lib查
 
然后在有此so库的目录, 进入python, 可以如下使用
>>> import hello
>>> hello.greet()
'hello, world'
 
4. python 调用 c++ (ctypes)
ctypes is an advanced ffi (Foreign Function Interface) package for Python 2.3 and higher. In Python 2.5 it is already included.
ctypes allows to call functions in dlls/shared libraries and has extensive facilities to create, access and manipulate simple and complicated C data types in Python - in other words: wrap libraries in pure Python. It is even possible to implement C callback functions in pure Python.
http://python.NET/crew/theller/ctypes/
 
#include <Python.h>

class TestFact{
    public:
    TestFact(){};
    ~TestFact(){};
    int fact(int n);
};

int TestFact::fact(int n)
{
  if (n <= 1)
    return 1;
  else
    return n * (n - 1);
}

extern "C"
int fact(int n)
{
    TestFact t;
    return t.fact(n);
}
将代码存为wrapper.cpp不用写python接口封装, 直接编译成so库,
g++ -fPIC wrapper.cpp -o example.so -shared -I/usr/include/python2.6 -I/usr/lib/python2.6/config
 
进入python, 可以如下使用
>>> import ctypes
>>> pdll = ctypes.CDLL('/home/ubuntu/tmp/example.so')
>>> pdll.fact(4)
12
下载 python可视化 https://www.youtube.com/playlist?list=PLO5e_-yXpYLAZhFhV6HMqziIPHUuA0Uu2
https://www.youtube.com/playlist?list=PLO5e_-yXpYLA7q3DFwSnIai5wsBN6lmw2
https://www.youtube.com/playlist?list=PLO5e_-yXpYLBxUo0gmygqDVdGPnRHryhs
https://www.youtube.com/playlist?list=PLO5e_-yXpYLDyeADG7xbFaJxvYyeAjHah
https://www.youtube.com/playlist?list=PLO5e_-yXpYLARtW5NPHTFVYY-xpgwuNNH
五子棋UI https://www.youtube.com/playlist?list=PLO5e_-yXpYLBMtzxaMcSe4sYmsVP7wVkv
django https://www.youtube.com/playlist?list=PLO5e_-yXpYLDFU9EEI8QSoxeWqxLF8rz4
suanfa
https://www.youtube.com/playlist?list=PLQEJNz6Rc2zdHkruJfQZIcTM__3ri9qGb：
豆瓣网：
sudo pip install -U wxpy -i https://pypi.doubanio.com/simple/
豆瓣网
cat ~/.bash_history |less 查看shell 输入记录

g++ -fPIC pycallclass.cpp -o libpycallclass.so  -shared -I/usr/include/python2.7
 -I/usr/lib/python2.7/config

1.	opncv ln -s /usr/local/Cellar/opencv/3.3.0_32/lib/python2.7/site-packages/cv.py cv.py  
2.	ln -s /usr/local/Cellar/opencv/3.3.0_3/lib/python2.7/site-packages/cv2.so cv2.so  
 




 
利用Boost.Python实现Python C/C++混合编程
2017-04-28 10:34 549人阅读 评论(0) 收藏 举报
  分类：
Python/C（1）   C++混合编程（1）  
版权声明：本文为博主原创文章，未经博主允许不得转载。
学习中如果碰到问题，参考官网例子：
D:\boost_1_61_0\libs\python\test
参考：Boost.Python 中英文文档。
利用Boost.Python实现Python C/C++混合编程
导出函数
#include<string> 
#include<boost/python.hpp>  
using namespace std; 
using namespace boost::python;  
 char const * greet() {     return "hello,world";  }  BOOST_PYTHON_MODULE(hello_ext) {     def("greet", greet); }

import hello_ext 
print hello_ext.greet()
导出类：
导出默认构造的函数的类




c++
#include<string> 
#include<boost/python.hpp>  
using namespace std; 
using namespace boost::python;  
struct World {     void set(string msg) { this->msg = msg; }    
string greet() { return msg; }      string msg; };  BOOST_PYTHON_MODULE(hello) //导出的module 名字 {     
class_<World>("World")         
.def("greet", &World::greet)         
.def("set", &World::set); }

python:
import hello 
planet = hello.World() # 调用默认构造函数，产生类对象 
planet.set("howdy")   # 调用对象的方法 
print planet.greet() # 调用对象的方法


导出：
#include<string>
#include<boost/python.hpp> 
 using namespace std; 
using namespace boost::python; 
 struct World {    
 World(string msg):msg(msg){} //增加构造函数     
World(double a, double b):a(a),b(b) {} //另外一个构造函数     
void set(string msg) { this->msg = msg; }     
string greet() { return msg; }     
double sum_s() { return a + b; }     
string msg;     double a;     double b; };  
BOOST_PYTHON_MODULE(hello) //导出的module 名字 {     class_<World>("World",init<string>())          
.def(init<double,double>()) 
// expose another construct         
.def("greet", &World::greet)         
.def("set", &World::set)         
.def("sum_s", &World::sum_s); }
python 测试调用：
import hello 
planet = hello.World(5,6) 
planet2 = hello.World("hollo world")  
print planet.sum_s() 
print planet2.greet()
如果不想导出任何构造函数，则使用no_init:
class_<Abstract>("Abstract",no_init)
#include<string> 
#include<boost/python.hpp>  
using namespace std; 
using namespace boost::python;   
struct Var 
{     
Var(string name):name(name),value(){}     
string const name;      
float value; };  
BOOST_PYTHON_MODULE(hello_var) 
{     class_<Var>("Var", init<string>())         
.def_readonly("name", &Var::name) //只读         
.def_readwrite("value", &Var::value); //读写 }
python调用:
import hello_var  
var = hello_var.Var("hello_var") 
var.value = 3.14        # var.name = 'hello' # error 
print var.name
C++类对象导出为Python的类对象，注意var.name不能赋值。
类的属性
// 类的属性  #include<string> 
#include<boost/python.hpp>  
using namespace std; 
using namespace boost::python;   
struct Num {     Num(){}     float get() const { return val; }     
void set(float val) { this->val = val; }     float val;  };  BOOST_PYTHON_MODULE(hello_num) {     class_<Num>("Num")         
.add_property("rovalue", &Num::get) 
// 对外：只读         
.add_property("value", &Num::get, &Num::set);// 对外读写 .value值会改变.rovalue值，存储着同样的数据。  }


python:
import hello_num num = hello_num.Num() num.value = 10 print num.rovalue #  result: 10
继承
// 类的继承  #include<string> 
#include<iostream> 
#include<boost/python.hpp>  
using namespace std; 
using namespace boost::python;  
struct Base 
{     
virtual ~Base() {};     
virtual string getName() { return "Base"; }      
string str; 
};  
struct Derived : Base 
{      
string getName() { return "Derived"; }  };   
void b(Base *base) { cout << base->getName() << endl; };  
void d(Derived *derived) 
{ 
cout << derived->getName() << endl; 
};  
Base * factory() 
{ return new Derived; }  /*     下面的额外的代码如果去掉会报错。     
解决地址：http://stackoverflow.com/questions/38261530/unresolved-external-symbols-since-visual-studio-2015-update-3-boost-python-link/38291152#38291152 */ 
namespace boost {     
template <>     
Base const volatile * get_pointer<class Base const volatile >
(class Base const volatile *c)     {         return c;     }
 }   
BOOST_PYTHON_MODULE(hello_derived) {    
 class_<Base>("Base")         
.def("getName", &Base::getName)         
.def_readwrite("str", &Base::str);      
 class_<Derived, bases<Base> >("Derived")         
.def("getName", &Derived::getName)         
.def_readwrite("str", &Derived::str);       
def("b", b);     
def("d", d);      
def("factory", factory, return_value_policy<manage_new_object>());// 
 }
python:
import hello_derived 
derive = hello_derived.factory() 
hello_derived.d(derive)
类的虚函数：
  /*  类的虚函数，实现的功能是：可以编写Python类，来继承C++类 */ #include<boost/python.hpp>  
#include<boost/python/wrapper.hpp> 
#include<string> #include<iostream>  
using namespace boost::python; 
using namespace std;  
struct Base {     
virtual ~Base() {}     
virtual int f() { return 0; }; };   
struct BaseWrap : Base, wrapper<Base> {   
  int f()     
{         
if (override f = this->get_override("f"))             
return f(); //如果函数进行重载了，则返回重载的         
return Base::f(); //否则返回基类     
}     
int default_f() { return this->Base::f(); } };  
BOOST_PYTHON_MODULE(hello_virtual) {     
class_<BaseWrap, boost::noncopyable>("Base")         
.def("f", &Base::f, &BaseWrap::default_f);   }
python：
import hello_virtual    
base = hello_virtual.Base() # 定义派生类，继承C++类 class Derived(hello_virtual.Base):     
def f(self):         
	return 42  
	derived = Derived()   
	print base.f()  
	print derived.f()
类的运算符/特殊函数
 // 类的运算符/特殊函数  
#include<string> 
#include<iostream>   
// #include<boost/python.hpp> 如果仅包含该头文件，会出错  
#include <boost/python/operators.hpp> 
#include <boost/python/class.hpp> 
#include <boost/python/module.hpp> 
#include <boost/python/def.hpp> 
#include <boost/operators.hpp>  
using namespace std; 
using namespace boost::python;  
class FilePos { 
public:     FilePos() :len(0) {}     
operator double()const { return len; };//重载类型转换符     
int len; };  // operator 方法  
FilePos operator+(FilePos pos, int a) 
{    
pos.len = pos.len + a;      return pos; //返回的是副本  
}  
FilePos operator+(int a, FilePos pos) 
{     
pos.len = pos.len + a;      return pos; //返回的是副本  
}   
int operator-(FilePos pos1, FilePos pos2) 
{      
return (pos1.len - pos2.len); 
 }  
FilePos operator-(FilePos pos, int a) 
{     
pos.len = pos.len - a;    
return pos; 
}  
	FilePos &operator+=(FilePos & pos, int a) 
	{     
	pos.len = pos.len + a;     
	return pos; 
	}  
FilePos &operator-=(FilePos & pos, int a) {     
	pos.len = pos.len - a;     
	return pos; }  
bool operator<(FilePos  pos1, FilePos pos2) {     
if (pos1.len < pos2.len)         
	return true;     
	return false; }   //特殊的方法  
FilePos pow(FilePos pos1, FilePos pos2) 
{     	FilePos res;     
	res.len = std::pow(pos1.len, pos2.len);     
	return res;  }
FilePos abs(FilePos pos) {     
	FilePos res;     
	res.len = std::abs(pos.len);      
	return res; 
}  
ostream& operator<<(ostream& out, FilePos pos) 
{     
	out << pos.len;     
	return out; 
}  
BOOST_PYTHON_MODULE(hello_operator) {     
class_<FilePos>("FilePos")         
	.def_readwrite("len",&FilePos::len)         
	.def(self + int())         
	.def(int() + self)         
	.def(self - self)         
	.def(self - int())         
	.def(self += int())         
	.def(self -= other<int>())         
	.def(self < self)         
	.def(float_(self))//特殊方法 ,     __float__         
	.def(pow(self, other<FilePos>()))  // __pow__         
	.def(abs(self))                    //  __abs__         
	.def(str(self));                //  __str__ for ostream   }
注意上面的：.def(pow(self, other<FilePos>()))模板后面要加上括号。也要注意头文件的包含，否则会引发错误。
python:
import hello_operator    
filepos1 = hello_operator.FilePos() 
filepos1.len = 10  
filepos2 = hello_operator.FilePos() 
filepos2.len = 20;  
print filepos1 - filepos2
函数
函数的调用策略。
 // 函数的调用策略   
#include<string> 
#include<iostream>  
#include<boost/python.hpp>  
using namespace std; 
using namespace boost::python;  
struct X {     string str; }; 
struct Z {     int value; };  
struct Y {     
	X x;     
	Z *z;     
	int z_value() 
	{ 
	return z->value; 
	} 
};  
X & f(Y &y, Z*z) {     
	y.z = z;     
	return y.x;  
//因为x是y的数据成员，x的声明周期与y进行了绑定。因为我们的目的是：Python接口//应尽可能的反映C++接口 
}   
BOOST_PYTHON_MODULE(hello_call_policy) {      
class_<Y>("Y")         
	.def_readwrite("x", &Y::x)         
	.def_readwrite("z", &Y::z)         
	.def("z_value", &Y::z_value);     
class_<X>("X")         
	.def_readwrite("str", &X::str);     
class_<Z>("Z")         
	.def_readwrite("value", &Z::value);     
// return_internal_reference<1 表示返回的值与第一个参数有关系：即第一个参数是//返回对象的拥有者（y和x都是引用的形式）。     
// with_custodian_and_ward<1, 2> 表示第二个参数的生命周期依赖于第一个参数的生命周期。     
def("f", f, return_internal_reference<1, with_custodian_and_ward<1, 2> >()); }
函数重载
// overloading  
#include<string> 
#include<iostream>  
#include<boost/python.hpp>  
using namespace std; 
using namespace boost::python;  
struct X {      
bool f(int a)     {         return true;     }     
bool f(int a, double b)     {         return true;     }     
bool f(int a, double b, char c)     {         return true;     }     
int f(int a, int b, int c)     {         return a + b + c;     } }; 
bool (X::*fx1)(int) = &X::f; 
bool(X::*fx2)(int, double) = &X::f; 
bool(X::*fx3)(int, double,char) = &X::f; 
I	nt(X::*fx4)(int, int,int) = &X::f;  

BOOST_PYTHON_MODULE(hello_overloaded) {     
class_<X>("X")         
	.def("f", fx1)         
	.def("f", fx2)         
	.def("f", fx3)         
	.def("f", fx4);  }

import hello_overloaded  
x = hello_overloaded.X() # create a new object   
print x.f(1)  # default 
int type print x.f(2,double(3)) 
print x.f(4,double(5),chr(6))  # chr(6) convert * to char  
print x.f(7,8,9)
认参数
普通函数的默认参数：
然而通过上面的方式对重载函数进行封装时，就丢失了默认参数的信息。当然我们可以通过一般形式的封装，如下：
int f(int,double = 3.14,
char const * = "hello"); 
int f1(int x){ return f(x);} 
int f2(int x,double y){return f(x,y)}  //int module 
init def("f",f); 
// 所有参数 
def("f",f2); //两个参数 
def("f",f1); //一个参数

但是通过上面的形式封装很麻烦。我们可以通过宏的形式，为我们批量完成上面的功能。
C++:
 // BOOST_PYTHON_FUNCTION_OVERLOADS  
#include<string> 
#include<iostream>  
#include<boost/python.hpp>   
using namespace std; 
using namespace boost::python;   
void foo(int a, char b = 1, unsigned c = 2, double d = 3) 
{     return; }  
BOOST_PYTHON_FUNCTION_OVERLOADS(foo_overloads, foo, 1, 4); 
// 参数个数的最小为1，最大为4  
BOOST_PYTHON_MODULE(hello_overloaded) {      
def("foo", foo, foo_overloads()); //实现导出带有默认参数的函数  }
python:
import hello_overloaded   
hello_overloaded.foo(1)  
hello_overloaded.foo(1,chr(2))  
hello_overloaded.foo(1,chr(2),3)  # 3对应的C++为unsigned int  hello_overloaded.foo(1,chr(2),3,double(4))
1
成员函数的默认参数：
 //使用BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS 宏，完成成员函数默认参数的接口  
#include<string> 
#include<iostream>  
#include<boost/python.hpp>   
using namespace std; 
using namespace boost::python;  
struct george {     
void wack_em(int a, int b = 0, char c = 'x')     
	{         
		return;    
 	}  
};   
BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(george_overloads, wack_em, 1, 3); // 参数个数的最小为1，最大为3  BOOST_PYTHON_MODULE(hello_member_overloaded) 
{      
class_<george>("george")         
	.def("wack_em", &george::wack_em, george_overloads());  
}
python:
import hello_member_overloaded  
c = hello_member_overloaded.george()  
c.wack_em(1) 
c.wack_em(1,2) 
c.wack_em(1,2,chr(3))
利用init和optional实现构造函数的重载。 
使用方法如下：
 // init  optional  
#include<string> 
#include<iostream> 
#include<boost/python.hpp>  
using namespace std; 
using namespace boost::python;  
struct X {     X(int a, char b = 'D', string c = "constructor", double b = 0.0) {} };  
BOOST_PYTHON_MODULE(hello_construct_overloaded) {     
class_<X>("X")         
.def(init<int, optional<char, string, double> >()); 
// init 和 optional  }
对象接口
Python 是动态类型的语言，C++是静态类型的。Python变量可能是：integer,float ,list ,dict,tuple,str,long,等等，还有其他类型。从Boost.Python和C++的观点来看，Python中的变量是类object的实例，在本节，我们看一下如何处理Python对象。

 // init  optional  
#include<string> 
#include<iostream> 
#include<boost/python.hpp> 
#include <numpy/arrayobject.h> 
using namespace std; 
using namespace boost::python;  
namespace bp = boost::python;   
void f(object x) 
	{     
	int y = extract<int>(x); // retrieve an int from x  
	}  
int g(object x) {     
extract<int> get_int(x);     
if (get_int.check())         
	return get_int();     
else         
	return 0; 
}   
int test(object &x) 
{    
	dict d = extract<dict>(x.attr("__dict__"));     
	d["whatever"] = 4;     
	return 0; 
}  
int test2(dict & d) 
	{     
		d["helloworld"] = 3;    
 		return 0;
 	} 
class A { 
 public:     
list lst;     
void listOperation(list &lst) {}; 
};  // 传入np.array数组对象，让C++进行处理 
int add_arr_1(object & data_obj, object rows_obj, object cols_obj) 
{     
PyArrayObject* data_arr =     reinterpret_cast<PyArrayObject*>(data_obj.ptr());     
float * data = static_cast<float *>(PyArray_DATA(data_arr));     
// using data     
int rows = extract<int>(rows_obj);     
int cols = extract<int>(cols_obj);     
for (int i = 0; i < rows*cols; i++)     
	{        
 	data[i] += 1;     
	}    
 return 0;  } 
BOOST_PYTHON_MODULE(hello_object) 
{     
def("test", test);     
def("test2", test2);     
def("add_arr_1", add_arr_1); 
}
python 调用：
import hello_object  
dic1 = {"whatever":1}  hello_object.test2(dic1)  
arr = np.array([1,2,3],dtype = float32)  
print arr.dtype  
print arr  hello_object.add_arr_1(arr,1,3)  
print arr


下面的是学C++时要注意的。
1.把C++当成一门新的语言学习（和C没啥关系！真的。）；
2.看《Thinking In C++》，不要看《C++变成死相》；
3.看《The C++ Programming Language》和《Inside The C++ Object
Model》,不要因为他们很难而我们自己是初学者所以就不看；
4.不要被VC、BCB、BC、MC、TC等词汇所迷惑——他们都是集成开发环境，而我们要学的是一门语言；
5.不要放过任何一个看上去很简单的小编程问题——他们往往并不那么简单，或者可以引伸出很多知识点；
6.会用Visual C++，并不说明你会C++；
7.学class并不难，template、STL、generic
programming也不过如此——难的是长期坚持实践和不遗余力的博览群书；
8.如果不是天才的话，想学编程就不要想玩游戏——你以为你做到了，其实你的C++水平并没有和你通关的能力一起变高——其实可以时刻记住：学C++是为了编游戏的；
9.看Visual C++的书，是学不了C++语言的；
10.浮躁的人容易说：XX语言不行了，应该学YY；——是你自己不行了吧！？
11.浮躁的人容易问：我到底该学什么；——别问，学就对了；
12.浮躁的人容易问：XX有钱途吗；——建议你去抢银行；
13.浮躁的人容易说：我要中文版！我英文不行！——不行？学呀！
14.浮躁的人容易问：XX和YY哪个好；——告诉你吧，都好——只要你学就行；
15.浮躁的人分两种：a)只观望而不学的人；b)只学而不坚持的人；
16.把时髦的技术挂在嘴边，还不如把过时的技术记在心里；
17.C++不仅仅是支持面向对象的程序设计语言；
18.学习编程最好的方法之一就是阅读源代码；
19.在任何时刻都不要认为自己手中的书已经足够了；
20.请阅读《The Standard C++ Bible》(中文版：标准C++宝典)，掌握C++标准；
21.看得懂的书，请仔细看；看不懂的书，请硬着头皮看；
22.别指望看第一遍书就能记住和掌握什么——请看第二遍、第三遍；
23.请看《Effective C++》和《More Effective C++》以及《Exceptional C++》；
24.不要停留在集成开发环境的摇篮上，要学会控制集成开发环境，还要学会用命令行方式处理程序；
25.和别人一起讨论有意义的C++知识点，而不是争吵XX行不行或者YY与ZZ哪个好；
26.请看《程序设计实践》，并严格的按照其要求去做；
27.不要因为C和C++中有一些语法和关键字看上去相同，就认为它们的意义和作用完全一样；
28.C++绝不是所谓的C的“扩充”——如果C++一开始就起名叫Z语言，你一定不会把C和Z语言联系得那么紧密；
29.请不要认为学过XX语言再改学C++会有什么问题——你只不过又在学一门全新的语言而已；
30.读完了《Inside The C++ Object Model》以后再来认定自己是不是已经学会了C++；
31.学习编程的秘诀是：编程，编程，再编程；http://hovertree.com/menu/cpp/
32.请留意下列书籍：《C++面向对象高效编程（C++ Effective Object-Oriented Software Construction）》《面向对象软件构造(Object-Oriented Software Construction)》《设计模式（Design Patterns）》《The Art of Computer Programming》；
33.记住：面向对象技术不只是C++专有的；
34.请把书上的程序例子亲手输入到电脑上实践，即使配套光盘中有源代码；
35.把在书中看到的有意义的例子扩充；
36.请重视C++中的异常处理技术，并将其切实的运用到自己的程序中；
37.经常回顾自己以前写过的程序，并尝试重写，把自己学到的新知识运用进去；
38.不要漏掉书中任何一个练习题——请全部做完并记录下解题思路；
39.C++语言和C++的集成开发环境要同时学习和掌握；
40.既然决定了学C++,就请坚持学下去，因为学习程序设计语言的目的是掌握程序设计技术，而程序设计技术是跨语言的；
41.就让C++语言的各种平台和开发环境去激烈的竞争吧，我们要以学习C++语言本身为主；
42.当你写C++程序写到一半却发现自己用的方法很拙劣时，请不要马上停手；请尽快将余下的部分粗略的完成以保证这个设计的完整性，然后分析自己的错误并重新设计和编写（参见43）；
43.别心急，设计C++的class确实不容易；自己程序中的class和自己的class设计水平是在不断的编程实践中完善和发展的；
44.决不要因为程序“很小”就不遵循某些你不熟练的规则——好习惯是培养出来的，而不是一次记住的；
45.每学到一个C++难点的时候，尝试着对别人讲解这个知识点并让他理解——你能讲清楚才说明你真的理解了；
46.记录下在和别人交流时发现的自己忽视或不理解的知识点；
47.请不断地对自己写的程序提出更高的要求,哪怕你的程序版本号会变成Version 100.XX；
48.保存好你写过的所有的程序——那是你最好的积累之一；
49.请不要做浮躁的人；
50.请热爱C++!
补充:
对c++学习的一点感想，希望对初学者能有些帮助
1.如果你以前从来没有接触过c++，那么选择的第一本c++教程就显得尤为重要，我认为你可以参照以下的标准进行选择：
a.对标准c++进行讲解，毕竟c++比从前发生了很大的变化。
b.要求全面，但不要很深，这要有助于你对于c++有一个全面的认识，打好基础，并且易懂的教材还能加快学习的进度，让自己保持一种成就感。
c.要有完整的范例来讲解每一个知识点如何运用，请注意这里所说的完整，并不是一个个代码片断。因为由于你以前从未接触过用c++进行编程，完整的代码可以使你有一个整体的概念，并且能够很快去进行大量的实践，因为变编程是从模仿开始，完整的代码恰恰告诉你了一个完整的步骤。不必自己去揣测。
d.推荐：《c++ primer plus》
2.当你有了一定的基础以后，就要选择一些书来迅速提高自己。这类书的特点是不仅仅教你如何去运用，而且要叫你如何去思考，并且你读起来也不是那么轻松。它意味深远，并不是你读一遍就能掌握的。
推荐：《thinking in c++》《effective c++》《more effective c++》
《c++ programming language》...《c++ 沉思录》
3.接下来就是对第二步所介绍的书籍进行反复的阅读，并且进行实践。由于这些书一位深远，每个人基于自己的基础都会有不同的收获，例如如果你的基础还没有达到某一高度，那么你就对一些精深的技术视而不见，不信？你可以试试，看看当自己有了一定提高之后再来读从前的一本书，你会发现许多新的东西。

	
豆瓣网：
sudo pip install -U wxpy -i https://pypi.doubanio.com/simple/
豆瓣网




