#include "clientMap.h"

void ClientMap::insert(char ID[], const char encryptedPwd[], int pos)
{
	ClientData *clientData = new ClientData(encryptedPwd, ID, pos);
	strcpy(clientData->history.selfID, ID);
	char selfID[110];
	strcpy(selfID, ID);
	hashMap.insert(make_pair(selfID, clientData));
}

void ClientMap::erase(char ID[])
{
	HashMap::const_iterator it = hashMap.find(ID);
	ClientData *data = it->second;
	delete data;
	hashMap.erase(ID);
}

ClientData::ClientData(const char pwd[], char ID[], int pos) : NTD(0), USdollar(0), RMB(0)
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
	for(auto it = hashMap.begin(); it != hashMap.end(); it++){
		printf("\tID = %s $ = %lld pwd = %s\n", it->first.ID, it->second->NTD, it->second->md5_password);	
	}
	printf("\n");
}


void ClientMap::yearEndBonus()
{
	boldBegin(YELLOW);
	printf("A year has passed.\nLike the final project in evil DSA course, we will give you bonus!!! Yeah~~~\nThe account that has more than 1000000 dollars can get a cherish number and attend the lottery.\n\n");
	syntaxEnd();
	int attendN = 0;
	char nameList[100][110];
	set<int> numberSet;

	for(auto it:hashMap)
	{
		if(it.second->NTD >= 1000000)
		{
			strcpy(nameList[attendN], it.second->selfID);
			attendN++;
		}
	}

	if(attendN == 0)
	{
		boldBegin(RED);
		printf("Nobody can attend, deposit more money next year!!\n");
		syntaxEnd();
		return;
	}
	//generate random numbers
	srand(time(NULL));
	while(numberSet.size() < attendN)
	{
		numberSet.insert(rand() % 1000000 + 1000000);
	}
	
	int draw = rand() % attendN;
	int drawNumber = 0;
	int index = 0;

	boldBegin(YELLOW);
	printf("Attendant and its number:\n");
	syntaxEnd();
	
	boldBegin(GREEN);
	for(auto it:numberSet)
	{
		printf("\t%s\t%d\n", nameList[index], it);
		index++;
		if(index == draw){
			drawNumber = it;
		}
	}
	syntaxEnd();
	boldBegin(YELLOW);
	printf("We are going to draw out a lucky person from them.\nDrawing....\n");
	this_thread::sleep_for(chrono::seconds(3));
	syntaxEnd();

	boldBegin(GREEN);
	printf("Congratulations!! Lottery number %d!! The owner is %s\nYour money in your account will times two~~~\n", drawNumber, nameList[draw]);
	hashMap.find(nameList[draw])->second->NTD *= 2;
	syntaxEnd();


}
void transferHistory(HistoryVec& fromH, char fromID[], HistoryVec& toH, char toID[], int time, LLI money)
{
	fromH.add(time, 0, toID, money);	//0:to
	toH.add(time, 1, fromID, money);	//1:from
	fromH.point(toH.getFTptr());
	toH.point(fromH.getFTptr());
}

void searchHistory(HistoryVec& h, char ID[])
{
	h.searchID(ID);
}

void mergeHistory(HistoryVec& a, HistoryVec& b)
{
	a = a.mergeVec(b);
}

void showHistory(HistoryVec&a)
{
	a.show();	
}

