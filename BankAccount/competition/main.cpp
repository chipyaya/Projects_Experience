#include <iostream>
#include <stdio.h>
#include <string.h>
#include "clientMap.h"
#include "md5cstr.h"
#include "nextWord.h"
//#include "ID_table.h"
using namespace std;
typedef long long int LLI;
int timeStamp = 1;
char lastID[110];

void login(ClientMap& clientMap, char ID[], char plainPwd[]) 
{
	ClientData *clientData = clientMap.search(ID);
	if (clientData == nullptr){
		printf("ID %s not found\n", ID);
		return;
	}
  char encryptedPwd[110]; md5(encryptedPwd, plainPwd);
	if (strcmp(clientData->md5_password, encryptedPwd) == 0)
	{
		strcpy(lastID, ID);
		//printf("lastID = %s\n", lastID);
		printf("success\n");
	}
 	else
   		printf("wrong password\n");
	return;
}

void create(ClientMap& clientMap, char ID[], char plainPwd[]) 
{
	//clientMap.showMap();
	if(clientMap.search(ID) != nullptr) {
		printf("ID %s exists, ", ID);
		// show 10 unused ID
    	int count = 0;
    	NextWordGenerator gen(ID);
    	while(count != 10)
    	{
     		char *next = gen.getNext();
     		if(clientMap.search(next) == nullptr) // if the ID doesn't exist, show it
      		{
        		printf("%s%c", next, (count == 9) ? '\n' : ',');
        		count++;
      		}
    	}
    		return;
	}
	char encryptedPwd[110]; md5(encryptedPwd, plainPwd);
	clientMap.insert(ID, encryptedPwd);
  	printf("success\n");
	return;
}

void remove(ClientMap& clientMap, char ID[], char plainPwd[]) 
{
  	ClientData *clientData = clientMap.search(ID);
	if (clientData == nullptr){
		printf("ID %s not found\n", ID);
		return;
	}
	char encryptedPwd[110]; md5(encryptedPwd, plainPwd);
	if (strcmp(clientData->md5_password, encryptedPwd) == 0){
		clientMap.erase(ID);
   		printf("success\n");
	}
 	else
   		printf("wrong password\n");
}

void deposit(ClientMap& clientMap, char ID[], LLI money)
{
	ClientData *clientData = clientMap.search(ID);
	clientData->money += money;
	printf("success, %lld dollars in current account\n", clientData->money);
	return;
}

void withdraw(ClientMap& clientMap, char ID[], LLI money)
{
	ClientData *clientData = clientMap.search(ID);
	if (clientData->money < money)
		printf("fail, %lld dollars only in current account\n", clientData->money);

	else{
		clientData->money -= money;
		printf("success, %lld dollars left in current account\n", clientData->money);
	}
	return;
}

void transfer(ClientMap& clientMap, char ID[], char transferID[], LLI money) 
{
	ClientData *clientData = clientMap.search(ID);
	ClientData *transferData = clientMap.search(transferID);
	if (transferData == nullptr){
		printf("ID %s not found, ", transferID);
		clientMap.recommendID(transferID);//recommendID
		//printf("\n");
		return;
	}

	if (clientData->money < money){
		printf("fail, %lld dollars only in current account\n", clientData->money);
		return;
	}
	
	clientData->money -= money;
	transferData->money += money;
	transferHistory(clientData->history, ID, transferData->history, transferID, timeStamp, money);
	timeStamp++;

	printf("success, %lld dollars left in current account\n", clientData->money);
}	

void merge(ClientMap& clientMap, char ID[], char password[], char ID_2[], char password_2[])
{
	ClientData *clientData_1 = clientMap.search(ID);
	ClientData *clientData_2 = clientMap.search(ID_2);
	if (clientData_1 == nullptr){
		printf("ID %s not found\n", ID);
		return;
	}

	if (clientData_2 == nullptr){
		printf("ID %s not found\n", ID_2);
		return;
	}
	char encryptedPwd_1[110]; md5(encryptedPwd_1, password);
	if (strcmp(clientData_1->md5_password, encryptedPwd_1) != 0){
		printf("wrong password1\n");
		return;
	}
	char encryptedPwd_2[110]; md5(encryptedPwd_2, password_2);
	if (strcmp(clientData_2->md5_password, encryptedPwd_2) != 0){
		printf("wrong password2\n");
		return;
	}

	clientData_1->money += clientData_2->money;
	mergeHistory(clientData_1->history, clientData_2->history);
	clientMap.erase(ID_2);
	printf("success, %s has %lld dollars\n", ID, clientData_1->money);
	return;
}

void search(ClientMap& clientMap, char ID[]){
	searchHistory(clientMap.search(lastID)->history, ID);
}


int main()
{

	char cmd[30];
	ClientMap clientMap;
	char ID[110], password[110];
	char ID_2[110], password_2[110];
	char transferID[110];
	char sth[110];
	LLI money;
	while (scanf("%s", cmd) != EOF){
		if (cmd[3] == 'i'){
			scanf("%s%s", ID, password);
			login(clientMap, ID, password);
		}
		else if (cmd[3] == 'a'){
			scanf("%s%s", ID, password);
			create(clientMap, ID, password);
		}
		else if (cmd[3] == 'e'){
			scanf("%s%s", ID, password);
			remove(clientMap, ID, password);
		}
		else if (cmd[3] == 'o'){
			scanf("%lld", &money);
			deposit(clientMap, lastID, money);
		}
		else if (cmd[3] == 'h'){
			scanf("%lld", &money);
			withdraw(clientMap, lastID, money);
		}
		else if (cmd[3]  == 'n'){
			scanf("%s%lld", transferID, &money);
			transfer(clientMap, lastID, transferID, money);
		}
		else if (cmd[3] == 'g'){
			scanf("%s%s%s%s", ID, password, ID_2, password_2);
			merge(clientMap, ID, password, ID_2, password_2);
		}
		else if (cmd[3] == 'r')
		{
			scanf("%s", ID);
			search(clientMap, ID);
		}
		else if (cmd[3] == 'd'){
			scanf("%s", sth);
			//find
			printf("\n");
		}
	}
}

