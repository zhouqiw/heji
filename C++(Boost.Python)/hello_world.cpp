#include <iostream>
#include <string>
#include <boost/python.hpp>
using namespace std;
using namespace boost::python;
void say()
{
    cout<<"Hello World!"<<endl;
}
void dog(){
cout<<"animals is good frinds"<<endl;


}




BOOST_PYTHON_MODULE(hello_world)
{
    def("say", say);
    def("dog",dog);
//    def("call", call);
}
