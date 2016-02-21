#include <iostream>
#include <stdio.h>
#include <assert.h>
#include "history.h"
#include "colorTerm.h"
using namespace std;

HistoryData* HistoryVec::getFTptr()
{
	return	historyV[historyV.size() - 1];
}

void HistoryVec::point(HistoryData *ptr){
	historyV[historyV.size() - 1]->FTptr = ptr;
	return;	
}

void HistoryVec::add(int _time, int _type, char _id[], LLI _money)
{
	HistoryData* newData = new HistoryData(_time, _type, _id, _money);
	historyV.push_back(newData);	
	size++;
}
HistoryVec HistoryVec::mergeVec(HistoryVec& other)	//&???
{
	HistoryVec h;
	strcpy(h.selfID, selfID);
	h.historyV.resize(size + other.size);
	h.size = size + other.size;
	int size1 = 0, size2 = 0;
	int i;
	for(i = 0; size1 < size && size2 < other.size && i < h.size; i++)
	{
		if(historyV[size1]->time < other.historyV[size2]->time)
		{
			h.historyV[i] = historyV[size1];
			size1++;
		}
		else if(historyV[size1]->time > other.historyV[size2]->time)
		{
			//not a, change the id of the pointed one to a
			if(strcmp(historyV[size1]->id, selfID) != 0)
			{
				strcpy(other.historyV[size2]->FTptr->id, selfID);
			}
			h.historyV[i] = other.historyV[size2];
			size2++;

		}
		else
		{
			//their time are the same=> mutual transfer
			//b->a
			if(strcmp(historyV[size1]->id, other.selfID) == 0)
			{
				strcpy(historyV[size1]->id, selfID); //change to a
			}
			h.historyV[i] = historyV[size1];
			i++;
			h.historyV[i] = other.historyV[size2];
			size1++;
			size2++;
				
		}
	}
	if(size1 == size)	//remain other's history
	{
		for(; i < h.size; i++)
		{
			strcpy(other.historyV[size2]->FTptr->id, selfID);
			h.historyV[i] = other.historyV[size2];
			size2++;
		}
	}
	else			//remain self's history
	{
		for(; i < h.size; i++)
		{
			if(strcmp(historyV[size1]->id, other.selfID) == 0)
			{
				strcpy(historyV[size1]->id, selfID);
			}

			h.historyV[i] = historyV[size1];
			size1++;
		}
	}
	return h;
}

void HistoryVec::searchID(char ID[])
{
	int found = 0;
	for(int i = 0; i < historyV.size(); i++)
	{
		assert(historyV.at(i) != NULL);
		if(strcmp(historyV[i]->id, ID) == 0)
		{
			found = 1;
			(historyV[i]->type == 0)? printf("To "):printf("From ");
			printf("%s %lld\n", historyV[i]->id, historyV[i]->money);
		}
	}
	if(found == 0)
	{
		printf("no record\n");	
	}
}


void HistoryVec::show()
{
	
	boldBegin(YELLOW);
	cout << "I'm " << selfID << endl;
	for(int i = 0; i < size; i++)
	{
		if(historyV[i]->type == 0)
			cout << "\tTo ";
		else if(historyV[i]->type == 1)
			cout << "\tFrom ";
		else
			cout << "Wrong type!!" << endl;
		
		cout << historyV[i]->money << endl;
	}
	syntaxEnd();
	cout << endl;
}


