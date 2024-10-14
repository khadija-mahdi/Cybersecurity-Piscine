#include <stdio.h>
#include <string.h>
int main(){
    char key[14] = "__stack_check";
    char input[100];
    printf("Please enter key: ");
    fscanf(stdin, "%s", input);
    if(strcmp(key, input) == 0){
        printf("Good job.\n");
        return 0;
    }
    printf("Nope.\n");
    return 0;
}