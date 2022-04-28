// Code getting from Book: Introduction to Genetic Algorithms - Germain Chartier
#include <stdio.h>
#include <curses.h>
#include <stdlib.h>
// gcc traveling_salesman_problem.c -lncurses # compile

int tsp[10][10] = {{999, 10, 3, 2, 5, 6, 7, 2, 5, 4},
                   {20, 999, 3, 5, 10, 2, 8, 1, 15, 6},
                   {10, 5, 999, 7, 8, 3, 11, 12, 3, 2},
                   {3, 4, 5, 999, 6, 4, 10, 6, 1, 8},
                   {1, 2, 3, 4, 999, 5, 10, 20, 11, 2},
                   {8, 5, 3, 10, 2, 999, 6, 9, 20, 1},
                   {3, 8, 5, 2, 20, 21, 999, 3, 5, 6},
                   {5, 2, 1, 25, 15, 10, 6, 999, 8, 1},
                   {10, 11, 6, 8, 3, 4, 2, 15, 999, 1},
                   {5, 10, 6, 4, 15, 1, 3, 5, 2, 999}};

int pa[1000][10] = {{0, 1, 2, 3, 4, 5, 6, 7, 8, 9},
                    {9, 8, 6, 3, 2, 1, 0, 4, 5, 7},
                    {2, 3, 5, 0, 1, 4, 9, 8, 6, 7},
                    {4, 8, 9, 0, 1, 3, 2, 5, 6, 7}};

int i, j, k, l, m, loc, flag, col, it, x = 3, y = 3;
int count, row = 0, res[1][10], row1, col1, z;
int numoff = 4;
int offspring[1000][10];
int mincost = 9999, mc;

void offcal1(int (*pa)[10]);
void offcal2(int (*pa)[10]);

int main(void)
{
    int gen;
    system("clear");
    printf("Number of generation: ");
    scanf("%d", &gen);
    offcal1(pa);
    offcal2(pa);
    printf("\n\t\t First Generation\n");
    for (i = 0; i < count; i++)
    {
        for (j = 0; j < 10; j++)
        {
            printf("%d", offspring[i][j]);
        }
        printf("\n");
    }

    for (y = 1; y <= gen - 1; y++)
    {
        getch();
        system("clear");
        for (i = 0; i < count; i++)
        {
            for (j = 0; j < 10; j++)
            {
                pa[i][j] = offspring[i][j];
            }
        }
        numoff = count;
        offcal1(pa);
        offcal2(pa);
        printf("\n\t\t %d Generation\n", y + 1);
        for (i = 0; i < count; i++)
        {
            for (j = 0; j < 10; j++)
            {
                printf("%d", offspring[i][j]);
            }
            printf("\n");
        }
        getch();
        system("clear");
    }
    printf("\n\nMinimum Cost Path\n");

    for (z = 0; z < 10; z++)
    {
        printf("%d ", res[0][z]);
    }
    printf("\nMinimum Cost %d \n", mincost);
}

/* finding the offspring using cyclic crossover */
void offcal1(int (*pa)[10])
{
    count = 0;
    for (i = 0; i < 1000; i++)
    {
        for (j = 0; j < 10; j++)
        {
            offspring[i][j] = -1;
        }
    }

    for (k = 0; k < numoff; k++)
    {
        for (l = k + 1; l < numoff; l++)
        {
            offspring[row][0] = pa[k][0];
            loc = pa[l][0];
            flag = 1;
            while (flag != 0)
            {
                for (j = 0; j < 10; j++)
                {
                    if (pa[k][j] == loc)
                    {
                        if (offspring[row][j] == -1)
                        {
                            offspring[row][j] = loc;
                            loc = pa[l][j];
                        }
                        else
                        {
                            flag = 0;
                        }
                    }
                }
            } /* end while */
            for (m = 0; m < 10; m++)
            {
                if (offspring[row][m] == -1)
                {
                    offspring[row][m] = pa[l][m];
                }
            }

            for (z = 0; z < 10; z++)
            {
                if (z < 9)
                {
                    row1 = offspring[row][z];
                    col1 = offspring[row][z + 1];
                    mc = mc + tsp[row1][col1];
                }
                else
                {
                    row1 = offspring[row][z];
                    col1 = offspring[row][0];
                    mc = mc + tsp[row1][col1];
                }
            }
            if (mc < mincost)
            {
                for (z = 0; z < 10; z++)
                {
                    res[0][z] = offspring[row][z];
                }
                mincost = mc;
            }
            count++;
            row++;
        } /* end l*/
    }
}

void offcal2(int (*pa)[10])
{
    for (k = 0; k < numoff; k++)
    {
        for (l = k + 1; l < numoff; l++)
        {
            offspring[row][0] = pa[l][0];
            loc = pa[k][0];
            flag = 1;
            while (flag != 0)
            {
                for (j = 0; j < 10; j++)
                {
                    if (pa[l][j] == loc)
                    {
                        if (offspring[row][j] == -1)
                        {
                            offspring[row][j] = loc;
                            loc = pa[k][j];
                        }
                        else
                        {
                            flag = 0;
                        }
                    }
                }
            } /* end while*/

            for (m = 0; m < 10; m++)
            {
                if (offspring[row][m] == -1)
                {
                    offspring[row][m] = pa[k][m];
                }
            }

            for (z = 0; z < 10; z++)
            {
                if (z < 9)
                {
                    row1 = offspring[row][z];
                    col1 = offspring[row][z + 1];
                    mc = mc + tsp[row1][col1];
                }
                else
                {
                    row1 = offspring[row][z];
                    col1 = offspring[row][0];
                    mc = mc + tsp[row1][col1];
                }
            }
            row++;
            if (mc < mincost)
            {
                for (z = 0; z < 10; z++)
                {
                    res[0][z] = offspring[row][z];
                }
                mincost = mc;
            }
            count++;
        } /* end l*/
    }
}