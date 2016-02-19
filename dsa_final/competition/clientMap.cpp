#include "clientMap.h"
#include <assert.h>
#include<queue>
#define NAMEMAX 101
const int LEN_SCORE[] = {0, 1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78, 91, 105, 120, 136, 153, 171, 190, 210, 231, 253, 276, 300, 325, 351, 378, 406, 435, 465, 496, 528, 561, 595, 630, 666, 703, 741, 780, 820, 861, 903, 946, 990, 1035, 1081, 1128, 1176, 1225, 1275, 1326, 1378, 1431, 1485, 1540, 1596, 1653, 1711, 1770, 1830, 1891, 1953, 2016, 2080, 2145, 2211, 2278, 2346, 2415, 2485, 2556, 2628, 2701, 2775, 2850, 2926, 3003, 3081, 3160, 3240, 3321, 3403, 3486, 3570, 3655, 3741, 3828, 3916, 4005, 4095, 4186, 4278, 4371, 4465, 4560, 4656, 4753, 4851, 4950, 5050};

void ClientMap::insert(char ID[], const char encryptedPwd[])
{
	ClientData *clientData = new ClientData(encryptedPwd, ID);
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

ClientData::ClientData(const char pwd[], char ID[]) : money(0)
{
  strcpy(md5_password, pwd);
  strcpy(selfID, ID);
}

ClientData* ClientMap::search(char ID[])
{
	HashMap::const_iterator it = hashMap.find(ID);
	if(it == hashMap.end())
	{
	  return nullptr;
	}  
	else
	{
	  return it->second;
	}
}

/*void ClientMap::showMap(){
	printf("Show Map:\n");
	for(auto it = hashMap.begin(); it != hashMap.end(); it++){
		printf("\tID = %s ID_addr = %d $ = %lld pwd = %s\n", it->first.ID, it->first.ID, it->second->money, it->second->md5_password);	
	}
	printf("\n");
}*/

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

class IDInfo{
public:
	char str[NAMEMAX];
	int score;
	
	IDInfo(){}

	IDInfo(char _str[], int _s)
	{
		strcpy(str, _str);
		score = _s;
	}
};

int calculateScore(const char a[], const char b[])
{
	int total = 0;
	int lenA = strlen(a), lenB = strlen(b);
	int minLen = (lenA < lenB) ? lenA : lenB;
 	int dlen = (lenA > lenB) ? (lenA - lenB) : (lenB - lenA);
  	total += LEN_SCORE[dlen];
  	for(int i = 0; i < minLen; i++)
    		total += (a[i] != b[i]) ? (minLen - i) : 0;
  	return total;
}

struct Compare {
    	bool operator()(IDInfo& a, IDInfo& b) 
    	{
       		if (a.score != b.score) 
			return a.score < b.score;
		else {
			if (strcmp(a.str, b.str) > 0)
				return false;
			else
				return true;
		}
	}
};

void ClientMap::recommendID(char transferID[])
{
	priority_queue<IDInfo, vector<IDInfo>, Compare> rID;
	vector<IDInfo> print_data;
	for(auto it = hashMap.begin(); it != hashMap.end(); it++)
	{
		if(rID.size() < 10){
			IDInfo *idInfo = new IDInfo;
			strcpy(idInfo->str, it->first.ID);
			idInfo->score = calculateScore(transferID, it->first.ID);
			rID.push(*idInfo);
		}
		else
		{
			int s = calculateScore(transferID, it->first.ID);
			if(s < rID.top().score || (s == rID.top().score && strcmp(it->first.ID, rID.top().str) < 0))
			{
				IDInfo *idInfo = new IDInfo;
				strcpy(idInfo->str, it->first.ID);
				idInfo->score = s;
				rID.pop();
				rID.push(*idInfo);
			}
		}
	}	

	for (int i = rID.size(); i > 0; i--){
		print_data.push_back(rID.top());
		rID.pop();
	}
	int size = print_data.size();
	assert(size < 11);
	for (int i = size-1; i >= 0; i--){
		printf("%s%c", print_data[i].str, (i >= 1)? ',':'\n');
	}
}
