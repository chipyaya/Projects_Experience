#define TRUE 1
#define FALSE 0
#define MAXVARS 10
#define MAX 2048

int popCount(unsigned);
int hammingWeight(int, int);
int contains(int, int, int, int);
void Quine_McCluskey(int, int, int[MAX][MAX], int*, int*, int*, int*, int&);
