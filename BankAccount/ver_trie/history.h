#ifndef HISTORY_VEC
#define HISTORY_VEC
#include <string.h>
#include <vector>
using namespace std;

typedef long long int LLI;

class HistoryData
{
public:
	int time;
	int type;	//0:to, 1:from
	char id[110];
	LLI money;
	HistoryData *FTptr;
	HistoryData(int _time, int _type, char _id[], LLI _money):time(_time), type(_type), money(_money), FTptr(nullptr){strcpy(id, _id);}
};

class HistoryVec
{
public:
	char selfID[110];
	int size;
	vector<HistoryData*> historyV;
	
	HistoryVec():size(0){}
	HistoryVec(char id[]):size(0){
		strcpy(selfID, id);	
	}
	
	void add(int _time, int _type, char _id[], LLI _money);
	
	HistoryData* getFTptr();
	void point(HistoryData *ptr);
	
	HistoryVec mergeVec(HistoryVec& other);
	
	void searchID(char ID[]);
	void show();
};


#endif
