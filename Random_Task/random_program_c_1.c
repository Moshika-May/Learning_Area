#include <stdio.h>

int main() {
    float f1;
    int f2;
    char f3[20];
    printf("Enter first float: ");
    scanf("%f", &f1);
    printf("Enter second int: ");
    scanf("%d", &f2);
    printf("Enter third char: ");
    scanf("%s", &f3);
    
    printf("===========================\n");
    printf("Float: %.2f\n", f1);
    printf("Int: %d\n", f2);
    printf("Char: %s\n", f3);
    return 0;
}























