#ifndef CLIENT_MAP
#define CLIENT_MAP

#include <stdio.h>
#include <iostream>
#include <map>
#include <string.h>

#include "ID_table.h"
#include "history.h"

using namespace std;

typedef long long int LLI;

class ClientData
{
public:
  LLI money; // < 10^10
  char md5_password[110];
  char selfID[110];		//for history use
  HistoryVec history;
  int IDpos;

  ClientData() : money(0) {}
  ClientData(const char pwd[], char ID[], int pos);
};

//for map

class CID{
public:
	char ID[110];
	CID(char* _id)
	{
		strcpy(ID, _id);
	}
	bool operator<(const CID& a)const
	{
		return strcmp(ID, a.ID) < 0;
	}


};

typedef map<CID, ClientData*> HashMap;

class ClientMap
{
private:
  HashMap hashMap;

public:
  void insert(char ID[], const char encryptedPwd[], int pos);
  void erase(char ID[]);

  // if not found return nullptr
  ClientData* search(char ID[]);
	void showMap();
};

void transferHistory(HistoryVec& fromH, char fromID[], HistoryVec& toH, char toID[], int time, LLI money);

void searchHistory(HistoryVec& h, char ID[]);
void mergeHistory(HistoryVec& a, HistoryVec& b);
#endif
