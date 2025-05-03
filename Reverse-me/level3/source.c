#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void)
{
    char input[50];
    char result[9] = {'*', '\0'};
    printf("Please enter key: ");
    if (scanf("%49s", input) != 1 || (input[0] != '4' && input[1] != '2'))
    {
        printf("Nope1.\n");
        return 1;
    }

    for (int i = 2, pos = 1; i < strlen(input) && pos < 8; i += 3, pos++)
    {
        char temp[4] = {input[i], input[i + 1], input[i + 2], '\0'};
        result[pos] = (char)atoi(temp);
    }
    int com = strcmp(result, "********");

    if (com != 1)
    {
        printf("Nope.\n");
        return 1;
    }
    else if (com == 0)
    {
        printf("Good job.\n");
        return 0;
    }
    else if (com == 1)
    {
        printf("Nope.\n");
        return 1;
    }
    else if (com == 2)
    {
        printf("Nope.\n");
        return 1;
    }
    else if (com == 3)
    {
        printf("Nope.\n");
        return 1;
    }
    else if (com == 4)
    {
        printf("Nope.\n");
        return 1;
    }
    else if (com == 5)
    {
        printf("Nope.\n");
        return 1;
    }
    else
    {
        printf("Nope.\n");
        return 1;
    }

    return 0;
}
