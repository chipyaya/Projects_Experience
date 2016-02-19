#include "clientMap.h"

void ClientMap::insert(char ID[], const char encryptedPwd[], int pos)
{
	ClientData *clientData = new ClientData(encryptedPwd, ID, pos);
	strcpy(clientData->history.selfID, ID);
	char selfID[110];
	strcpy(selfID, ID);
	tries.insert(selfID, clientData);
}

void ClientMap::erase(char ID[])
{
	tries.erase(ID);
}

ClientData::ClientData(const char pwd[], char ID[], int pos) : money(0)
{
  strcpy(md5_password, pwd);
  strcpy(selfID, ID);
  IDpos = pos;
}

ClientData* ClientMap::search(char ID[])
{
  ClientData *desiredData;
	if(tries.search(ID, desiredData))
	  return desiredData;
	else
	  return nullptr;
}

void transferHistory(HistoryVec& fromH, char fromID[], HistoryVec& toH, char toID[], int time, LLI money)
{
	fromH.add(time, 0, toID, money);	//0:to
	toH.add(time, 1, fromID, money);	//1:from
	fromH.point(toH.getFTptr());
	toH.point(fromH.getFTptr());
	//fromH.show();
	//toH.show();
}

void searchHistory(HistoryVec& h, char ID[])
{
	//h.show();
	h.searchID(ID);
}

void mergeHistory(HistoryVec& a, HistoryVec& b)
{
	a = a.mergeVec(b);
	//a.show();
}
