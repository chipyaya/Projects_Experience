#include <iostream>
using namespace std;
#define NUM 1000000

int main(){
	string cmd[50] = {"login", "create", "delete", "deposit", "withdraw", "transfer", "merge", "search", "find"};
	for(int i = 0; i < 8; i++){
		for(int j = 0; j < NUM; j++)
			cout << cmd[i] << endl;
	
	}



}
