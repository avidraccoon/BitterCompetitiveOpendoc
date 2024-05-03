#include <iostream>
#include "core.h"

using namespace std;

class Test{
	public:
	string test;
};

void print(string str){
	cout << str;
}

void println(string str){
	cout << str << "\n";
}

int main(){
	ArrayList<string> test;
	test.add("Hello World");
	print("testing ");
	println(test.get(0));
	return 0;
}

