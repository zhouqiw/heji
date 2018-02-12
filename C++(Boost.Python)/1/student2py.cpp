
#include <boost/python.hpp>
#include <iostream>
#include <string>
using namespace std;
using namespace boost::python;

class student
{
public:
    void setname(string str)
    {
        name_ = str;
    }
    
    string getname()
    {
        return name_;
    }
    
    void setage(int age)
    {
        age_ = age;
    }
    
    int getage()
    {
        return age_;
    }
    
private:
    string name_;
    int age_;
    
}


BOOST_PYTHON_MODULE(example)  //python模块
{
    
 class_<student>("student")
.def(setname,&student::setname)
.def(getname,&student::getname)
.def(setage,&student::setage)
.def(getage,&student::getage)
.add_property(name,&student::getname,&student::setname)
.add_property(age,&student::getage,&student::setage)
;
}
