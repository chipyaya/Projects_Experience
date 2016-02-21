#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <vector>

#include "nextWord.h"
using std::vector; using std::abs;

Word::Word(char *s) : isEmpty(false)
{
  strcpy(str, s);
}

void Word::createCounter()
{
  for(char *p = str; *p != '\0'; p++)
    if(*p == '?')
      charPos.push_back(p - str);
  counter.resize(charPos.size());
  modify();
}

void Word::add()
{
  if(charPos.size() == 0)
  {
    isEmpty = true;
    return;
  }
  counter[0] ++;
  for(size_t i = 0; i < counter.size() - 1; i++)
    if(counter[i] >= BASE)
    {
      counter[i + 1] += counter[i] / BASE;
      counter[i] %= BASE;
    }

  if(counter[counter.size() - 1] >= BASE)
    isEmpty = true;
}

inline void Word::modify()
{
  for(size_t i = 0; i < charPos.size(); i++)
    str[charPos[i]] = ASCII_TABLE[counter[i]];
}

inline void Word::update()
{
  add();
  if(!isEmpty)
    modify();
}


NextWordGenerator::NextWordGenerator(char *_compareStr) : score(1), minIndex(-1)
{
  strLen = strlen(_compareStr);
  strcpy(compareStr, _compareStr);
  getPattern(wordTable, compareStr, strLen, score);
}

void NextWordGenerator::updateScore()
{
  minIndex = -1;
  score++;
  wordTable.clear();
  getPattern(wordTable, compareStr, strLen, score);
}

char* NextWordGenerator::getNext()
{
  char *next = nullptr;
  while(next == nullptr)
  {
    next = getNextWordWithThisScore();
    if(next == nullptr)
      updateScore();
  }
  return next;
}
char* NextWordGenerator::getNextWordWithThisScore()
{
  while(true)
  {
    if(minIndex != -1)
      wordTable[minIndex].update();

    char *min = nullptr;
    for(size_t i = 0; i < wordTable.size(); i++)
    {
      if(wordTable[i].isEmpty)
        continue;
      if(min == nullptr || strcmp(min, wordTable[i].str) > 0)
      {
        min = wordTable[i].str;
        minIndex = i;
      }
    }

    // cannot generate more words
    if(min == nullptr)
      return min;

    // return this word
    if(calScore(min, compareStr) == score)
      return min;
  }
}


int calScore(char *a, char *b)
{
  int total = 0;
  int lenA = strlen(a), lenB = strlen(b);
  int minLen = (lenA < lenB) ? lenA : lenB;
  int dlen = (lenA > lenB) ? (lenA - lenB) : (lenB - lenA);
  total += LEN_DIFF_SCORE[dlen];
  for(int i = 0; i < minLen; i++)
    total += (a[i] != b[i]) ? (minLen - i) : 0;
  return total;
}

void generateDiffPostion(vector<vector<int>> &martix, vector<int> &vec, int quota, int nowTryPos)
{  
  if(quota > nowTryPos)
  {
    // choose
    vec.push_back(nowTryPos);
    generateDiffPostion(martix, vec, quota - nowTryPos, nowTryPos + 1); 
    vec.pop_back();

    // not choose
    generateDiffPostion(martix, vec, quota, nowTryPos + 1); 
  }
  else if(quota == nowTryPos)
  {
    // save answer into martix
    vec.push_back(nowTryPos);
    martix.push_back(vec);
    vec.pop_back();
  }
}

void generateDiffMartix(vector<vector<int>> &martix, int dposScore)
{
  vector<int> tempVector;
  if(dposScore == 0)
  {
    tempVector.push_back(0);
    martix.push_back(tempVector);
  }
  else
    generateDiffPostion(martix, tempVector, dposScore, 1);
}

inline void lengthenWord(char *str, const int strLen, int lengthenLen, vector<int> &dpos)
{
  // modify position
  for(size_t i = 0; i < dpos.size(); i++)
    str[strLen - dpos[i]] = '?';
  // modify length
  for(int i = 0; i < lengthenLen; i++)
    str[strLen + i] = '?';
  str[strLen + lengthenLen] = '\0';
}

inline void shortenWord(char *str, const int strLen, int shortenLen, vector<int> &dpos)
{
  // modify postion
  for(size_t i = 0; i < dpos.size(); i++)
    str[strLen - shortenLen - dpos[i]] = '?';
  // modify length
  str[strLen - shortenLen] = '\0';
}

void getPattern(vector<Word> &table, char *str, const int strLen, const int score)
{
  for(int dlen = 0; dlen < LEN_DIFF_SCORE_SIZE && LEN_DIFF_SCORE[dlen] <= score; dlen++)
  {
    int dposScore = score - LEN_DIFF_SCORE[dlen];

    vector<vector<int>> dposMartix;
    generateDiffMartix(dposMartix, dposScore);

    // try each combinations
    for(size_t i = 0; i < dposMartix.size(); i++)
    {
      int maxdpos = dposMartix[i].back();
      // shorten word
      if(dlen < strLen && strLen - dlen - maxdpos >= 0)
      {
        table.push_back(Word(str));
        shortenWord(table.back().str, strLen, dlen, dposMartix[i]);
        table.back().createCounter();
      }
      // lengthen word
      if(dlen != 0 && strLen - maxdpos >= 0) 
      {
        table.push_back(Word(str));
        lengthenWord(table.back().str, strLen, dlen, dposMartix[i]);
        table.back().createCounter();
      }

    }

  }
}
