#ifndef TRIES
#define TRIES

#include <cstdio>
#include <cstdlib>
#include <utility>
const char ascii2index[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0, 0, 0, 0, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 0, 0, 0, 0, 0, 0, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 0, 0, 0, 0};
const int ascii2index_SIZE = sizeof(ascii2index) / sizeof(ascii2index[0]);
const int MAX_CHILDREN = 62;
const int MAX_STRLEN = 100;
template <typename Data>
struct Tries
{
public:
  struct Node
  {
    Node *children[MAX_CHILDREN];
    int size;
    bool isExist;
    Data data;

    Node() : size(0), isExist(false) 
    {
      for(int i = 0; i < MAX_CHILDREN; i++)
        children[i] = nullptr;
    }

    ~Node()
    {
      for(int i = 0; i < MAX_CHILDREN; i++)
      {
        if(children[i] == nullptr)
          continue;
        children[i]->~Node();
      }
    }

    void insert(char *p, Data &insertData)
    {
      if(*p == '\0')
      {
        isExist = true;
        data = insertData;
        return;
      }

      int index = ascii2index[int(*p)];
      if(children[index] == nullptr)
      {
        children[index] = new Node;
        size++;
      }

      children[index]->insert(p + 1, insertData);
    }

    // is last ptr can delete ?
    bool erase(char *p)
    {
      if(*p == '\0')
      {
        isExist = false;
        if(size == 0)
          return true; // last node can delete ptr to this node
        else 
          return false;
      }

      int index = ascii2index[int(*p)];

      if(children[index]->erase(p + 1))
      {
        size--;
        delete children[index];
        children[index] = nullptr;
        if(size == 0 && isExist == false)
          return true; // last node can delete ptr to this node
      }

      return false;
    }

    Data* search(char *p)
    {
      if(*p == '\0')
      {
        if(isExist)
          return &data;
        else 
          return nullptr;
      }

      int index = ascii2index[int(*p)];
      if(children[index] == nullptr)
        return nullptr;
      else
        return children[index]->search(p + 1);
    }
    

  };

  Node *root;

  Tries()
  {
    root = new Node;
  }

  ~Tries()
  {
    delete root;
  }

  void insert(char *str, Data insertData)
  {
    root->insert(str, insertData);
  }

  void erase(char *str)
  {
    root->erase(str);
  }

  bool search(char *str, Data &retData)
  {
    Data *foundDataPtr = root->search(str);
    if(foundDataPtr== nullptr)
      return false;
    retData = *foundDataPtr;
    return true;
  }

};

#endif
