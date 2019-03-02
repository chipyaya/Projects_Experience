#ifndef CLIENT_MAP
#define CLIENT_MAP

#include <stdio.h>
#include <iostream>
#include <string.h>
#include "tries.h"
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




class ClientMap
{
private:
  Tries<ClientData *> tries;

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
