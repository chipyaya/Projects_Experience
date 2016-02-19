#include "ID_table.h"
int TABLE::insert(char* ID)
{
	int len = strlen(ID);
	IDinfor temp;
	strncpy(temp.str, ID, len + 1);
	ID_table[len].push_back(temp);
	return ID_table[len].size() - 1;
}

char* TABLE::eraser(int pos, int len)
{
	if (pos == ID_table[len].size() - 1){
		ID_table[len].pop_back();
		return NULL;
	}

	strncpy(ID_table[len][pos].str, ID_table[len].back().str, len + 1);
	ID_table[len].pop_back();
	return ID_table[len][pos].str;
}

bool cmp (IDinfor a, IDinfor b)
{ 
	if (strcmp(a.str, b.str) > 0)
		return false;
	else
		return true;	
}

void print( vector <IDinfor> & print_data)
{
	if (print_data.empty()){
		printf("\n");
		return;
	}
	int size = print_data.size();
	for (int i = 0; i < size; i++){
		printf("%s%c", print_data[i].str, (i < size - 1)? ',':'\n');
	}
	
}

bool hasStart(char* wildcard_ID, int len)
{
	for (int i = 0; i < len; i++)
		if (wildcard_ID[i] == '*')
			return true;
	return false;
}

void TABLE::find(char* wildcard_ID, char* lastID)
{
	vector<IDinfor> print_data;
	int len = strlen(wildcard_ID);
	if (hasStart(wildcard_ID, len)){
		for (int i = 1; i < NAMEMAX; i++){
			int size = ID_table[i].size();
			for (int j = 0; j < size; j++){
				if (strcmp(ID_table[i][j].str, lastID) == 0)
					continue;
				if (WildTextCompare(ID_table[i][j].str, wildcard_ID))
					print_data.push_back(ID_table[i][j]);
			}
		}
	}

	else {
		int size = ID_table[len].size();
		for (int i = 0; i < size; i++){
			if (strcmp(ID_table[len][i].str, lastID) == 0)
					continue;
			if (WildTextCompare(ID_table[len][i].str, wildcard_ID))
				print_data.push_back(ID_table[len][i]);
		}
	}

	sort(print_data.begin(), print_data.end(), cmp);
	print(print_data);
}

int calculateScore(char *a, char *b)
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
    	bool operator()(IDinfor& a, IDinfor& b) 
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

void recommend(vector<IDinfor>& ID_len_table, priority_queue<IDinfor, vector<IDinfor>, Compare>& rID, char* ID)
{
	int size = ID_len_table.size();
	for (int i = 0; i < size; i++){
		if (rID.size() < 10){
			ID_len_table[i].score = calculateScore(ID, ID_len_table[i].str);
			rID.push(ID_len_table[i]);
		}
		else {
			ID_len_table[i].score = calculateScore(ID, ID_len_table[i].str);
			IDinfor temp = rID.top();
			if (temp.score < ID_len_table[i].score)
				continue;
			else if (temp.score > ID_len_table[i].score){
				rID.pop();
				rID.push(ID_len_table[i]);
			}

			else {
				if (strcmp(temp.str, ID_len_table[i].str) > 0){
					rID.pop();
					rID.push(ID_len_table[i]);
				}
			}
		}
	}
}

/*void TABLE::recommendID(char* ID)
{
	int len = strlen(ID);
	priority_queue<IDinfor, vector<IDinfor>, Compare> rID;
	vector<IDinfor> print_data;
	
	recommend(ID_table[len], rID, ID);
	int x = 1;
	while (x < LEN_SCORE_SIZE && (rID.size() < 10 || rID.top().score >= LEN_SCORE[x])){
		if (len - x > 0)
			recommend(ID_table[len - x], rID, ID);
		//if (len + x <= 100)
			recommend(ID_table[len + x], rID, ID);
		x++;
	}

	for (int i = rID.size(); i > 0; i--){
		print_data.push_back(rID.top());
		rID.pop();
	}
	
	//sort(print_data.begin(), print_data.end(), cmp);
	printf("ID %s not found, ", ID);
	for (int i = print_data.size() - 1; i >= 0; i--)
		printf("%s%c", print_data[i].str, (i > 0)? ',':'\n');
};*/

void TABLE::recommendID(char* ID)
{
	priority_queue<IDinfor, vector<IDinfor>, Compare> rID;
	vector<IDinfor> print_data;
	for (int i = 1; i < NAMEMAX; i++)
		recommend(ID_table[i], rID, ID);


	for (int i = rID.size(); i > 0; i--){
		print_data.push_back(rID.top());
		rID.pop();
	}
	
	//sort(print_data.begin(), print_data.end(), cmp);
	printf("ID %s not found, ", ID);
	for (int i = print_data.size() - 1; i >= 0; i--)
		printf("%s%c", print_data[i].str, (i > 0)? ',':'\n');
};
