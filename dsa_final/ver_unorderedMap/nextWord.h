#ifndef NEXT_WORD
#define NEXT_WORD

#include <cstring>
#include <vector>
using std::vector;

const int MAX_STRING_LEN = 200;

const int LEN_DIFF_SCORE[] = {0, 1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78, 91};
const int LEN_DIFF_SCORE_SIZE = sizeof(LEN_DIFF_SCORE) / sizeof(LEN_DIFF_SCORE[0]);
const char ASCII_TABLE[] = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
const int ASCII_TABLE_SIZE = sizeof(ASCII_TABLE) / sizeof(ASCII_TABLE[0]) - 1; // not to count '\0'

struct Word
{
  bool isEmpty;
  char str[MAX_STRING_LEN + 1];
  const int &BASE = ASCII_TABLE_SIZE;
  vector<int> charPos;
  vector<int> counter;

  Word(char *s);
  void createCounter();
  void add();
  inline void modify();
  inline void update();
};

struct NextWordGenerator
{
  vector<Word> wordTable;
  char compareStr[MAX_STRING_LEN + 1];
  int score;
  int minIndex;
  int strLen;

  NextWordGenerator(char *_compareStr);
  void updateScore();
  char* getNext();
  char *getNextWordWithThisScore();
};

void lengthenWord(char *ans, const int len, int dlen, vector<int> &dpos);
void shortenWord(char *ans, const int len, int dlen, vector<int> &dpos);
void generateDiffPostion(vector<vector<int>> &martix, vector<int> &vec, int quota, int nowTryPos);
void generateDiffMartix(vector<vector<int>> &martix, int dposScore);
int calScore(char *a, char *b);
void getPattern(vector<Word> &table, char *str, const int strLen, const int score);

#endif
