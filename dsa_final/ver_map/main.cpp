#include <iostream>
#include <stdio.h>
#include <string.h>
#include "clientMap_Map.h"
#include "md5cstr.h"
#include "nextWord.h"
#include "ID_table.h"
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

void create(ClientMap& clientMap, char ID[], char plainPwd[], TABLE& id_table) 
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
	int pos = id_table.insert(ID);
	char encryptedPwd[110]; md5(encryptedPwd, plainPwd);
    	clientMap.insert(ID, encryptedPwd, pos);
  	printf("success\n");
	return;
}

void remove(ClientMap& clientMap, char ID[], char plainPwd[], TABLE &id_table) 
{
  	ClientData *clientData = clientMap.search(ID);
	if (clientData == nullptr){
		printf("ID %s not found\n", ID);
		return;
	}
	char encryptedPwd[110]; md5(encryptedPwd, plainPwd);
	if (strcmp(clientData->md5_password, encryptedPwd) == 0){
		char* tempID = id_table.eraser(clientData->IDpos, strlen(ID));
		if (tempID != NULL){
			ClientData *clientData_2 = clientMap.search(tempID);
			clientData_2->IDpos = clientData->IDpos;
		}
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

void transfer(ClientMap& clientMap, char ID[], char transferID[], LLI money, TABLE& id_table)
{
	ClientData *clientData = clientMap.search(ID);
	ClientData *transferData = clientMap.search(transferID);
	if (transferData == nullptr){
		id_table.recommendID(transferID);
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

void merge(ClientMap& clientMap, char ID[], char password[], char ID_2[], char password_2[], TABLE &id_table)
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
	char* tempID = id_table.eraser(clientData_2->IDpos, strlen(ID_2));
	if (tempID != NULL){
		ClientData *backID_clientData = clientMap.search(tempID);
		backID_clientData->IDpos = clientData_2->IDpos;
	}
	clientMap.erase(ID_2);
	printf("success, %s has %lld dollars\n", ID, clientData_1->money);
	return;
}

void search(ClientMap& clientMap, char ID[]){
	//ClientData *clientData = clientMap.search(ID);
	//if (clientData == nullptr){
		//cout << "ID " << ID <<" not found" << endl;
	//	return;
	//}
	searchHistory(clientMap.search(lastID)->history, ID);
	
}


int main()
{

	char cmd[30];
	ClientMap clientMap;
	TABLE id_table;
	char ID[110], password[110];
	char ID_2[110], password_2[110];
	char transferID[110];
	char sth[110];
	LLI money;
	while (scanf("%s", cmd) != EOF){
		if (strcmp(cmd, "login") == 0){
			scanf("%s%s", ID, password);
			login(clientMap, ID, password);
		}
		else if (strcmp(cmd, "create") == 0){
			scanf("%s%s", ID, password);
			create(clientMap, ID, password, id_table);
		}
		else if (strcmp(cmd, "delete") == 0){
			scanf("%s%s", ID, password);
			remove(clientMap, ID, password, id_table);
		}
		else if (strcmp(cmd, "deposit") == 0){
			scanf("%lld", &money);
			deposit(clientMap, lastID, money);
		}
		else if (strcmp(cmd, "withdraw") == 0){
			scanf("%lld", &money);
			withdraw(clientMap, lastID, money);
		}
		else if (strcmp(cmd, "transfer") == 0){
			scanf("%s%lld", transferID, &money);
			transfer(clientMap, lastID, transferID, money, id_table);
		}
		else if (strcmp(cmd, "merge") == 0){
			scanf("%s%s%s%s", ID, password, ID_2, password_2);
			merge(clientMap, ID, password, ID_2, password_2, id_table);
		}
		else if (strcmp(cmd, "search") == 0)
		{
			scanf("%s", ID);
			search(clientMap, ID);
		}
		else if (strcmp(cmd, "find") == 0){
			scanf("%s", sth);
			id_table.find(sth, lastID);
		}
		else
		{
			printf("Wrong command!!!!!!!!!!!!!!!\n");	
		}
		//clientMap.showMap();
	}
}

