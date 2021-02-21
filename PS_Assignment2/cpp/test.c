#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <windows.h>

#include "arralloc.h"
#include "uni.h"
#include "percolate.h"

void measure_time(int);

void main()
{
	measure_time(200);
}


void measure_time(int range) {
    double timesum;
    LARGE_INTEGER time_start;	//开始时间
    LARGE_INTEGER time_over;	//结束时间
    double dqFreq;		//计时器频率
    LARGE_INTEGER f;	//计时器频率
    QueryPerformanceFrequency(&f);
    dqFreq=(double)f.QuadPart;
    
    int length[range+1];
	for(int i=1;i<range+1;i++)
	{
		length[i] = i;
	}
	
	double run_time[range];
	for(int i=1;i<range+1;i++)
	{	
		for(int j=0;j<20;j++)
		{
			QueryPerformanceCounter(&time_start);	//计时开始
			percolate(length[i]);
			QueryPerformanceCounter(&time_over);	//计时结束
			timesum += 1000000*(time_over.QuadPart-time_start.QuadPart)/dqFreq;
			//乘以1000000把单位由秒化为微秒，精度为1000 000/（cpu主频）微秒
		}
		run_time[i] = timesum/10;
		//printf("run_time for %d:%f us\n",i,run_time[i]);
		//printf("-------------\n");
	}
	
	char* dataFile = "run_time";
	FILE *fp;
	fp = fopen(dataFile, "w");
	for (int i=1; i<=range; i++)
	{
		  fprintf(fp, " %.4f\n", run_time[i]);
	}
	fclose(fp);	
	
	printf("Finish");
}
