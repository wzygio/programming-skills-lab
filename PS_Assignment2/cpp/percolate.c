#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include "arralloc.h"
#include "uni.h"
#include "percolate.h"

void percolate(int length)
{
	//int length;
	int** map;
	float rho;
	int seed;
	int maxClusters;
	char* datFile;
	char* pgmFile;
	
	// length = 20; //define the default value
	rho  = 0.30; 
	seed = 1564;
	datFile = "map.dat";
	pgmFile = "map.pgm";
	maxClusters = length * length;
	
	/*
	printf("Rho (density): %f\n", rho);
	printf("Map width/height: %d\n", length);
	printf("Seed: %d\n", seed);
	printf("Maximum number of clusters: %d\n", maxClusters);
	printf("Data file: %s\n", datFile);
	printf("PGM file: %s\n", pgmFile);
	*/
	
	map = (int**)arralloc(sizeof(int), 2, length + 2, length + 2);
	
	//随即初始化为1或0
	rinit(seed);
	
	int nfill;
	int i, j;
	float r;
	for (i=0; i<length+2; i++)
	{
	  for (j=0; j<length+2; j++)
		{
		  map[i][j] = 0;
		}
	}
	nfill = 0;
	for (i=1; i<=length; i++)
	{
	  for (j=1; j<=length; j++)
		{
		  r=random_uniform();
		  if(r > rho)
		    {
		      nfill++;
		      map[i][j]=1;
		    }
		}
	}
	//printf("rho = %f, actual density = %f\n", rho, 1.0 - ((double) nfill)/((double) length*length) );
	
	//为每个方块赋予一个唯一的编号
	nfill = 0;
	for (i=1; i<=length; i++)
	{
	  for (j=1; j<=length; j++)
		{
		  if (map[i][j] != 0)
		    {
		      nfill++;
		      map[i][j] = nfill;
		    }
		}
	}
	
	//迭代：将每个方块中的值替换为四个邻居中最大的值
	int loop, nchange, old;
	loop = 1;
	nchange = 1;
	while (nchange > 0)
	{
	  nchange = 0;//每次循环前陡降change数归0
	  for (i=1; i<=length; i++)
		{
		  for (j=1; j<=length; j++)
		    {
		      if (map[i][j] != 0)
			{
			  old = map[i][j];
			  if (map[i-1][j] > map[i][j]) map[i][j] = map[i-1][j];
			  if (map[i+1][j] > map[i][j]) map[i][j] = map[i+1][j];
			  if (map[i][j-1] > map[i][j]) map[i][j] = map[i][j-1];
			  if (map[i][j+1] > map[i][j]) map[i][j] = map[i][j+1];
			  if (map[i][j] != old)
			    {
			      nchange++;
			    }
			}
		    }
		}
	  //printf("Number of changes on loop %d is %d\n", loop, nchange);
	  loop++;
	}
	
	//检测是否渗透（percs），并记录渗透集群对应的数值（percclusternum）
	int itop, ibot, percclusternum;
	int percs = 0;
	percclusternum = 0;
	for (itop=1; itop<=length; itop++)
	{
	  if (map[1][itop] > 0)
		{
		  for (ibot=1; ibot<=length; ibot++)
		    {
		      if (map[1][itop] == map[length][ibot])
				{
				  percs = 1;
				  percclusternum = map[itop][length];
				}
		    }
		}
	}
	if (percs)
	{
	  //printf("Cluster DOES percolate. Cluster number: %d\n", percclusternum);
	}
	else
	{
	  //printf("Cluster DOES NOT percolate\n");
	}
	
	//写入结果
	//printf("Opening file %s\n", datFile);
	FILE *fp;
	fp = fopen(datFile, "w");
	//printf("Writing data ...\n");
	for (i=1; i<=length; i++)
	{
	  for (j=1; j<=length; j++)
		{
		  fprintf(fp, " %4d", map[i][j]);
		}
	  fprintf(fp,"\n");
	}
	//printf("...done\n");
	fclose(fp);
	//printf("Closed file %s\n", datFile);
	
	//计算cluster size，cluster number，rank，并上色
	int ncluster, maxsize;
	struct cluster *clustlist;
	int colour;
	int *rank;
	clustlist = (struct cluster*)arralloc(sizeof(struct cluster), 1, length*length);
	rank = (int*)arralloc(sizeof(int), 1, length*length);
	for (i=0; i < length*length; i++)
	{
	  rank[i] = -1;
	  clustlist[i].size = 0;
	  clustlist[i].id   = i+1;
	}
	for (i=1;i<=length; i++)
	{
	  for (j=1; j<=length; j++)
		{
		  if (map[i][j] != 0)
		    {
		      ++(clustlist[map[i][j]-1].size);
		    }
		}
	}

	//按照clustersize排序
	percsort(clustlist, length*length);//调用percsort
	maxsize = clustlist[0].size;
	for (ncluster=0; ncluster < length*length && clustlist[ncluster].size > 0; ncluster++);
	if (maxClusters > ncluster)
	{
	  maxClusters = ncluster;
	}
	for (i=0; i < ncluster; i++)
	{
	  rank[clustlist[i].id - 1] = i;
	}
	//printf("Opening file %s\n", pgmFile);
	fp = fopen(pgmFile, "w");
	//printf("Map has %d clusters, maximum cluster size is %d\n", ncluster, maxsize);

	//生成图像 
	if (maxClusters == 1)
	{
	  //printf("Displaying the largest cluster\n");
	}
	else if (maxClusters == ncluster)
	{
	  //printf("Displaying all clusters\n");
	}
	else
	{
	  //printf("Displaying the largest %d clusters\n", maxClusters);
	}
	//printf("Writing data ...\n");
	fprintf(fp, "P2\n");
	if (maxClusters > 0)
	{
	  fprintf(fp, "%d %d\n%d\n", length, length, maxClusters);
	}
	else
	{
	  fprintf(fp, "%d %d\n%d\n", length, length, 1);
	}
	for (i=1; i<=length; i++)
	{
	  for (j=1; j<=length; j++)
		{
		  if (map[i][j] > 0)
		    {
		      colour = rank[map[i][j]-1];
		      if (colour >= maxClusters)
				{
				  colour = maxClusters;
				}
		    }
		  else
		    {
		      colour = maxClusters;
		    }
		  fprintf(fp, " %4d", colour);
		}
	  fprintf(fp,"\n");
	}
	//printf("...done\n");
	fclose(fp);
	//printf("Closed file %s\n", pgmFile);
	free(clustlist);
	free(rank);
	
	free(map);
}

static int clustcompare(const void *p1, const void *p2)
{
	int size1, size2, id1, id2;
	
	size1 = ((struct cluster *) p1)->size;
	size2 = ((struct cluster *) p2)->size;
	
	id1   = ((struct cluster *) p1)->id;
	id2   = ((struct cluster *) p2)->id;
	
	if (size1 != size2)
	{
	  return(size2 - size1);
	}
	else
	{
	  return(id2 - id1);
	}
}

void percsort(struct cluster *list, int n)
{
	qsort(list, (size_t) n, sizeof(struct cluster), clustcompare);
}
