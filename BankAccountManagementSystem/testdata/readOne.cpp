#include <stdio.h>
#include <string.h>
#include <time.h>
int main(){
	clock_t start = clock();
	char cmd[50];
	while(scanf("%s", cmd) !=EOF){
	if (cmd[3] == 'i'){} else if (cmd[3] == 'a'){}	else if (cmd[3] == 'e'){} else if (cmd[3] == 'o'){} else if (cmd[3] == 'h'){} else if (cmd[3]  == 'n'){} else if (cmd[3] == 'g'){} else if (cmd[3] == 'r'){} else if (cmd[3] == 'd'){}	
	}
	clock_t finish = clock();
	printf("%f\n", (double)(finish - start) / CLOCKS_PER_SEC);

}


