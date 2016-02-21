#include <stdio.h>
#include <time.h>
#include <string.h>
int main(){
	clock_t start = clock();
	char cmd[50];
	while(scanf("%s", cmd) !=EOF){
		if (strcmp(cmd, "login") == 0){
		}
		else if (strcmp(cmd, "create") == 0){
		}
		else if (strcmp(cmd, "delete") == 0){
		}
		else if (strcmp(cmd, "deposit") == 0){
		}
		else if (strcmp(cmd, "withdraw") == 0){
		}
		else if (strcmp(cmd, "transfer") == 0){
		}
		else if (strcmp(cmd, "merge") == 0){
		}
		else if (strcmp(cmd, "search") == 0){
		}
		else if (strcmp(cmd, "find") == 0){
		}
	}
	clock_t finish = clock();
	printf("%f\n", (double)(finish - start) / CLOCKS_PER_SEC);

}


