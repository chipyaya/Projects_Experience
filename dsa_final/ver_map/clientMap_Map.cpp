#include "clientMap_Map.h"

void ClientMap::insert(char ID[], const char encryptedPwd[], int pos)
{
	ClientData *clientData = new ClientData(encryptedPwd, ID, pos);
	strcpy(clientData->history.selfID, ID);
	char selfID[110];
	strcpy(selfID, ID);
	//printf("%s\n", selfID);
	hashMap.insert(make_pair(selfID, clientData));
}

void ClientMap::erase(char ID[])
{
	HashMap::const_iterator it = hashMap.find(ID);
	ClientData *data = it->second;
	delete data;
	hashMap.erase(ID);
}

ClientData::ClientData(const char pwd[], char ID[], int pos) : money(0)
{
  strcpy(md5_password, pwd);
  strcpy(selfID, ID);
  IDpos = pos;
}

ClientData* ClientMap::search(char ID[])
{
	HashMap::const_iterator it = hashMap.find(ID);
	if(it == hashMap.end())
	{
	  //printf("not exist\n");
	  return nullptr;
	}  
	else
	{
	  //printf("exist\n");
	  return it->second;
	}
}

void ClientMap::showMap(){
	printf("Show Map:\n");
	for(HashMap::iterator it = hashMap.begin(); it != hashMap.end(); it++){
		printf("\tID = %s ID_addr = %d $ = %lld pwd = %s\n", it->first.ID, it->first.ID, it->second->money, it->second->md5_password);	
		//printf("\tID = %s ID_addr = %d $ = %lld pwd = %s\n", it->first, it->first, it->second->money, it->second->md5_password);	
	}
	printf("\n");
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
