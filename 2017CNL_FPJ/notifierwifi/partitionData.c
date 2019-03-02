#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <time.h>

#define ITER 400
#define MAXLEN 64

int main(int argc, char const *argv[]){
	
	srand(time(NULL));
	
	FILE *readFp = fopen("./data","r");
	assert(readFp != NULL);
	FILE *trainingFp = fopen("./ML/train_data","w");
	assert(trainingFp != NULL);
	FILE *validationFp = fopen("./ML/validate_data","w");
	assert(validationFp != NULL);
	
	char line[MAXLEN];
	int trainCount = 0,valCount = 0;
	for(int i = 0;i < ITER;i++){
		int r = rand()%5;
		fgets(line,MAXLEN,readFp);
		if(r == 0 && valCount < (ITER / 5)){
			fputs(line,validationFp);
			valCount++;
		}
		else if(trainCount >= (ITER / 5 * 4)){
			fputs(line,validationFp);
			valCount++;
		}
		else{
			fputs(line,trainingFp);
			trainCount++;
		}
	}
	return 0;
}