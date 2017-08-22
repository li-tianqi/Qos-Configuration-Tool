/*********************************************************************************/
/* test c read csv                                                               */
/*********************************************************************************/

#include <stdio.h>
#include <unistd.h>
#include <string.h>

int main(int argc, char* argv[]){
	
	int n = 4000;	
	//int i;
	
	//int k = 0x00c8;
	
	char sh_pir_csv_path[1024];  // pir csv file path
	
	{
		int count;
		count = readlink("/proc/self/exe", sh_pir_csv_path, 1024);  // get this file's path
		
		// remove this file's name
		for(int i=strlen(sh_pir_csv_path); i>0; i--)
			if( sh_pir_csv_path[i] == '/')
			{
				sh_pir_csv_path[i]='\0';
				break;
			}
		
		// add csv file's name
		strcat(sh_pir_csv_path, "/sh_pir.csv"); 
	}
	
	// printf("%s\n", sh_pir_csv_path);
	
	
	int pir[n];  // save pir value from csv file
	
	{
		//read sh_pir.csv file
		FILE *fp;
		char temp_pir[n][20];

		//read csvfile line by line
		fp = fopen(sh_pir_csv_path, "r");
		for(int i = 0; i < n; i++) {
			fgets(temp_pir[i], 20, fp);
		}
		fclose(fp);

		//transform string to int
		for(int i = 0; i < n; i++) {
			sscanf(temp_pir[i], "%x", &pir[i]);
		}
	}
	
	//printf("k=%d\n", k);
	
	
	//printf("path=%s\n",argv[0]);
	
	// test
	while(1){
		int key;
		printf("input shaper id (0-3999):");
		scanf("%d",&key);
		printf("0x%x\n", pir[key]);
		//printf("%d\n", key);
		
		
	}
	
	return 0;
}