#ifndef CLIENT_MAP
#define CLIENT_MAP

#include <stdio.h>
#include <iostream>
#include <unordered_map>
#include <string.h>
#include<queue>

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
  ClientData(const char pwd[], char ID[]);
};

//for unordered_map

class CID{
public:
	char ID[110];
	CID(char* _id)
	{
		strcpy(ID, _id);
	}
	bool operator=(const CID& a)const
	{
		return strcmp(ID, a.ID) == 0;
	}


};


struct my_equal_to {  
    bool operator()(const CID& x, const CID& y) const  
    {
		return strcmp( x.ID, y.ID ) == 0; 
	}  
};

struct Hash_Func
{
    //BKDR hash algorithm
    int operator()(CID cid)const
    {
        int seed = 131;//31  131 1313 13131131313 etc//
        int hash = 0;
	int i = 0;
        while(cid.ID[i])
        {
            hash = (hash * seed) + (cid.ID[i]);
            i++;
        }

        return hash & (0x7FFFFFFF);
    }
};

typedef unordered_map<CID, ClientData*, Hash_Func, my_equal_to > HashMap;

class ClientMap
{
private:
  HashMap hashMap;

public:
  void insert(char ID[], const char encryptedPwd[]);
  void erase(char ID[]);

  // if not found return nullptr
  ClientData* search(char ID[]);
	void showMap();
	void recommendID(char transferID[]);
};

void transferHistory(HistoryVec& fromH, char fromID[], HistoryVec& toH, char toID[], int time, LLI money);

void searchHistory(HistoryVec& h, char ID[]);
void mergeHistory(HistoryVec& a, HistoryVec& b);
#endif
