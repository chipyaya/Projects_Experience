#include <iostream>
#include <thread>
#include <chrono>

#include <stdio.h>
#include <string.h>
#include <assert.h>
#include "clientMap.h"
#include "md5cstr.h"
#include "nextWord.h"
#include "ID_table.h"
#include "colorTerm.h"

using namespace std;

typedef long long int LLI;

int timeStamp = 1;
char lastID[110];
LLI NTD = 100000;
LLI USdollar = 100000;
LLI RMB = 100000;



void wait()
{
	boldBegin(YELLOW);
	printf("You've got wrong pwd for more than 3 times.\nPlease wait for 10 secs before the next operation.\n");
	syntaxEnd();
	for(int i = 10; i > 0; i--)
	{
		boldBegin(YELLOW);
		printf("%d\n", i);
		syntaxEnd();
		this_thread::sleep_for(chrono::seconds(1));
	}
	boldBegin(YELLOW);
	printf("Try again now.\n");
	syntaxEnd();
	return;

}



void login(ClientMap& clientMap, char ID[], char plainPwd[]) 
{
	ClientData *clientData = clientMap.search(ID);
	if (clientData == nullptr){
		boldBegin(RED);
		printf("ID %s not found\n", ID);
		syntaxEnd();
		return;
	}

	char encryptedPwd[110]; 
	md5(encryptedPwd, plainPwd);

	if (strcmp(clientData->md5_password, encryptedPwd) == 0)
	{
		strcpy(lastID, ID);
		boldBegin(GREEN);
		printf("success\n");
		syntaxEnd();
	}
 	else
  	{
		boldBegin(RED);
   		printf("wrong password\n");
		syntaxEnd();

		clientData->wrongTimes++;
		if(clientData->wrongTimes > 3)
		{
			wait();
		}

  	}	
	return;
}

void create(ClientMap& clientMap, char ID[], char plainPwd[], TABLE& id_table) 
{
	//clientMap.showMap();
	if(clientMap.search(ID) != nullptr) {
		boldBegin(YELLOW);
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
		syntaxEnd();
    		return;
	}
	int pos = id_table.insert(ID);
	char encryptedPwd[110]; md5(encryptedPwd, plainPwd);
  	clientMap.insert(ID, encryptedPwd, pos);
	boldBegin(GREEN);
  	printf("success\n");
  	syntaxEnd();
	return;
}

void remove(ClientMap& clientMap, char ID[], char plainPwd[], TABLE &id_table) 
{
  	ClientData *clientData = clientMap.search(ID);
	if (clientData == nullptr){
	  	boldBegin(RED);
		printf("ID %s not found\n", ID);
    		syntaxEnd();
		return;
	}
	char encryptedPwd[110]; md5(encryptedPwd, plainPwd);
	if (strcmp(clientData->md5_password, encryptedPwd) == 0){
		char* tempID = id_table.eraser(clientData->IDpos, strlen(ID));
		if (tempID != NULL){
			ClientData *clientData_2 = clientMap.search(tempID);
			clientData_2->IDpos = clientData->IDpos;
		}
		NTD -= clientData->NTD;
		clientMap.erase(ID);
		boldBegin(GREEN);
   		printf("success\n");
      		syntaxEnd();
	}
 	else
  	{
	  	boldBegin(RED);
   		printf("wrong password\n");
      		syntaxEnd();
  	}
}

void deposit(ClientMap& clientMap, char ID[], LLI money)
{
	if (strcmp(lastID, "*") == 0)
		return;
	ClientData *clientData = clientMap.search(ID);
	clientData->NTD += money;
	NTD += money;
	boldBegin(GREEN);
	printf("success, %lld dollars in current account\n", clientData->NTD);
  	syntaxEnd();
	return;
}

void withdraw(ClientMap& clientMap, char ID[], LLI money)
{
	if (strcmp(lastID, "*") == 0)
		return;
	ClientData *clientData = clientMap.search(ID);
	if (clientData->NTD < money)
  	{
    		boldBegin(RED);
		printf("fail, %lld dollars only in current account\n", clientData->NTD);
    		syntaxEnd();
  	}
	else{
		clientData->NTD -= money;
		NTD -= money;
    		boldBegin(GREEN);
		printf("success, %lld dollars left in current account\n", clientData->NTD);
    		syntaxEnd();
	}
	return;
}

void transfer(ClientMap& clientMap, char ID[], char transferID[], LLI money, TABLE& id_table)
{
	if (strcmp(lastID, "*") == 0)
		return;
	ClientData *clientData = clientMap.search(ID);
	ClientData *transferData = clientMap.search(transferID);
	if (transferData == nullptr){
    		boldBegin(YELLOW);
		id_table.recommendID(transferID);
    		syntaxEnd();
		return;
	}

	if (clientData->NTD < money){
    		boldBegin(RED);
		printf("fail, %lld dollars only in current account\n", clientData->NTD);
    		syntaxEnd();
		return;
	}
	
	clientData->NTD -= money;
	transferData->NTD += money;
	transferHistory(clientData->history, ID, transferData->history, transferID, timeStamp, money);
	timeStamp++;
  	boldBegin(GREEN);
	printf("success, %lld dollars left in current account\n", clientData->NTD);
  	syntaxEnd();
}	

void merge(ClientMap& clientMap, char ID[], char password[], char ID_2[], char password_2[], TABLE &id_table)
{
	ClientData *clientData_1 = clientMap.search(ID);
	ClientData *clientData_2 = clientMap.search(ID_2);
	if (clientData_1 == nullptr){
    		boldBegin(RED);
		printf("ID %s not found\n", ID);
    		syntaxEnd();
		return;
	}

	if (clientData_2 == nullptr){
    		boldBegin(RED);
		printf("ID %s not found\n", ID_2);
    		syntaxEnd();
		return;
	}
	char encryptedPwd_1[110]; md5(encryptedPwd_1, password);
	if (strcmp(clientData_1->md5_password, encryptedPwd_1) != 0){
    		boldBegin(RED);
		printf("wrong password1\n");
    		syntaxEnd();
		return;
	}
	char encryptedPwd_2[110]; md5(encryptedPwd_2, password_2);
	if (strcmp(clientData_2->md5_password, encryptedPwd_2) != 0){
    		boldBegin(RED);
		printf("wrong password2\n");
    		syntaxEnd();
		return;
	}

	clientData_1->NTD += clientData_2->NTD;
	mergeHistory(clientData_1->history, clientData_2->history);
	char* tempID = id_table.eraser(clientData_2->IDpos, strlen(ID_2));
	if (tempID != NULL){
		ClientData *backID_clientData = clientMap.search(tempID);
		backID_clientData->IDpos = clientData_2->IDpos;
	}
	clientMap.erase(ID_2);
	boldBegin(GREEN);
	printf("success, %s has %lld dollars\n", ID, clientData_1->NTD);
	syntaxEnd();
	return;
}

void search(ClientMap& clientMap, char ID[]){
	if (strcmp(lastID, "*") == 0)
		return;
	boldBegin(WHITE);
	searchHistory(clientMap.search(lastID)->history, ID);
	syntaxEnd();
}

void showMoney(ClientMap &clientMap, char ID[])
{
	if (strcmp(lastID, "*") == 0)
		return;
	ClientData *clientData = clientMap.search(ID);
	boldBegin(YELLOW);
	printf("There are %lld NTD in your account.\n", clientData->NTD);
	printf("There are %lld USdollar in your account.\n", clientData->USdollar);
	printf("There are %lld RMB in your account.\n", clientData->RMB);
	syntaxEnd();

}

void changePassword(ClientMap &clientMap, char ID[])
{
	if (strcmp(lastID, "*") == 0)
		return;
	ClientData *clientData = clientMap.search(ID);
	char password[110];
	int time = 0;
	boldBegin(YELLOW);
	printf("Please input your old password.\n");
	syntaxEnd();
	scanf("%s", password);
	char encryptedPwd[110]; 
	md5(encryptedPwd, password);
	while (strcmp(clientData->md5_password, encryptedPwd) != 0){
    		boldBegin(RED);
		printf("wrong password\n");
    		syntaxEnd();
		time++;
		if (time == 4){
			boldBegin(YELLOW);
			printf("You've got wrong pwd for more than 3 times.\n");
			printf("already logout your account.\n");
			printf("Please login again.\n");
			syntaxEnd();
			strcpy(lastID, "*");
			return;
		}

		boldBegin(YELLOW);
		printf("Please input your old password again.\n");
		syntaxEnd();
		scanf("%s", password);
		char encryptedPwd[110]; 
		md5(encryptedPwd, password);
	}
	
	boldBegin(YELLOW);
	printf("please input your new password.\n");
	syntaxEnd();
	scanf("%s", password);
	char encryptedPwd_new[110]; 
	md5(encryptedPwd_new, password);
	strcpy(clientData->md5_password, encryptedPwd_new);
	assert(strcmp(clientData->md5_password, encryptedPwd_new) == 0);
	boldBegin(GREEN);
   	printf("success\n");
      	syntaxEnd();
}

double compute_exchange_rate(LLI currency_1, LLI currency_2)
{
	double dif = (double)currency_2 / (double)currency_1;
	return dif;
}

void ForeignCurrencyExchange(ClientMap &clientMap, char *currency_1, char *currency_2, LLI money, char ID[])
{
	if (strcmp(lastID, "*") == 0)
		return;
	if (strcmp(currency_1, currency_2) == 0){
		boldBegin(RED);
		printf("fail, both currency are same\n");
    		syntaxEnd();
		return;
	}
	ClientData *clientData = clientMap.search(ID);
	if (strcmp(currency_1, "NTD") == 0){
		if (clientData->NTD < money){
			boldBegin(RED);
			printf("fail, %lld NTD only in current account\n", clientData->NTD);
			syntaxEnd();
			return;
		}

		else {
			if (strcmp(currency_2, "USdollar") == 0){
				double exchange_rate = compute_exchange_rate(NTD, USdollar);
				clientData->NTD -= money;
				NTD -= money;
				USdollar += (LLI)(money * exchange_rate);
				clientData->USdollar += (LLI)(money * exchange_rate);
				boldBegin(GREEN);
   				printf("success\n");
      				syntaxEnd();
				printf("There are %lld NTD in your account.\n", clientData->NTD);
				printf("There are %lld USdollar in your account.\n", clientData->USdollar);
				return;
			}

			else if (strcmp(currency_2, "RMB") == 0){
				double exchange_rate = compute_exchange_rate(NTD, RMB);
				clientData->NTD -= money;
				NTD -= money;
				RMB += (LLI)(money * exchange_rate);
				clientData->RMB += (LLI)(money * exchange_rate);
				boldBegin(GREEN);
   				printf("success\n");
      				syntaxEnd();
				printf("There are %lld NTD in your account.\n", clientData->NTD);
				printf("There are %lld RMB in your account.\n", clientData->RMB);
				return;
			}
		}
	}

	if (strcmp(currency_1, "USdollar") == 0){
		if (clientData->USdollar < money){
			boldBegin(RED);
			printf("fail, %lld USdollar only in current account\n", clientData->USdollar);
			syntaxEnd();
			return;
		}

		else {
			if (strcmp(currency_2, "NTD") == 0){
				double exchange_rate = compute_exchange_rate(USdollar, NTD);
				clientData->USdollar -= money;
				USdollar -= money;
				NTD += (LLI)(money * exchange_rate);
				clientData->NTD += (LLI)(money * exchange_rate);
				boldBegin(GREEN);
   				printf("success\n");
      				syntaxEnd();
				printf("There are %lld USdollar in your account.\n", clientData->USdollar);
				printf("There are %lld NTD in your account.\n", clientData->NTD);
				return;
			}

			else if (strcmp(currency_2, "RMB") == 0){
				double exchange_rate = compute_exchange_rate(USdollar, RMB);
				clientData->USdollar -= money;
				USdollar -= money;
				RMB += (LLI)(money * exchange_rate);
				clientData->RMB += (LLI)(money * exchange_rate);
				boldBegin(GREEN);
   				printf("success\n");
      				syntaxEnd();
				printf("There are %lld USdollar in your account.\n", clientData->USdollar);
				printf("There are %lld RMB in your account.\n", clientData->RMB);
				return;
			}
		}
	}

	if (strcmp(currency_1, "RMB") == 0){
		if (clientData->RMB < money){
			boldBegin(RED);
			printf("fail, %lld RMB only in current account\n", clientData->NTD);
			syntaxEnd();
			return;
		}

		else {
			if (strcmp(currency_2, "USdollar") == 0){
				double exchange_rate = compute_exchange_rate(RMB, USdollar);
				clientData->RMB -= money;
				RMB -= money;
				USdollar += (LLI)(money * exchange_rate);
				clientData->USdollar += (LLI)(money * exchange_rate);
				boldBegin(GREEN);
   				printf("success\n");
      				syntaxEnd();
				printf("There are %lld RMB in your account.\n", clientData->RMB);
				printf("There are %lld USdollar in your account.\n", clientData->USdollar);
				return;
			}

			else if (strcmp(currency_2, "NTD") == 0){
				double exchange_rate = compute_exchange_rate(RMB, NTD);
				clientData->RMB -= money;
				RMB -= money;
				NTD += (LLI)(money * exchange_rate);
				clientData->NTD += (LLI)(money * exchange_rate);
				boldBegin(GREEN);
   				printf("success\n");
      				syntaxEnd();
				printf("There are %lld RMB in your account.\n", clientData->RMB);
				printf("There are %lld NTD in your account.\n", clientData->NTD);
				return;
			}
		}
	}

	printf("fail, the currency is wrang.\n");
}

void ShowExchangeRate()
{
	printf("NTD to USdollar : %lf\n", compute_exchange_rate(NTD, USdollar));
	printf("NTD to RMB : %lf\n", compute_exchange_rate(NTD, RMB));
	printf("USdollar to NTD : %lf\n", compute_exchange_rate(USdollar, NTD));
	printf("USdollar to RMB : %lf\n", compute_exchange_rate(USdollar, RMB));
	printf("RMB to NTD : %lf\n", compute_exchange_rate(RMB, NTD));
	printf("RMB to USdollar : %lf\n", compute_exchange_rate(RMB, USdollar));
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
		else if (strcmp(cmd, "find") == 0)
		{
			scanf("%s", sth);
			id_table.find(sth, lastID);
		}
		else if (strcmp(cmd, "showMoney") == 0)
		{
			showMoney(clientMap, lastID);

		}
		else if (strcmp(cmd, "changePassword") == 0)
		{
			changePassword(clientMap, lastID);
		}
		else if (strcmp(cmd, "yearEndBonus") == 0)
		{
			clientMap.yearEndBonus();	
		}
		else if (strcmp(cmd, "showHistory") == 0)
		{
			showHistory(clientMap.search(lastID)->history);
		}
		else if (strcmp(cmd, "ForeignCurrencyExchange") == 0)
		{
			char currency_1[20];
			char currency_2[20];
			scanf("%s%s%lld", currency_1, currency_2, &money);
			ForeignCurrencyExchange(clientMap, currency_1, currency_2, money, lastID);
		}
		else if (strcmp(cmd, "ShowExchangeRate") == 0)
		{
			ShowExchangeRate();
		}
		else
		{
      			boldBegin(RED);
			printf("Wrong command!!!!!!!!!!!!!!!\n");	
      			syntaxEnd();
		}
		//clientMap.showMap();
	}
}

