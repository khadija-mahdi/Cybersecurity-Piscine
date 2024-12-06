#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int main(void) {
    char input[50];
    char result[9] = "d";
    
    printf("Please enter key: ");
    if (scanf("%49s", input) != 1 || input[0] != '0' || input[1] != '0') {
        printf("Nope.\n");
        return 1;
    }

    for (int i = 2, pos = 1; i < strlen(input) && pos < 8; i += 3, pos++) {
        char temp[4] = {input[i], input[i + 1], input[i + 2], '\0'};
        result[pos] = (char)atoi(temp);
    }

    if (strcmp(result, "delabere") == 0) {
        printf("Good job.\n");
        return 0;
    } else {
    printf("Nope.\n");
    return 0;
    }

    return 0;
}
