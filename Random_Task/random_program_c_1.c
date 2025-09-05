#include <math.h>
#include <stdio.h>
#include <stdlib.h>

int main()
{
    int PI;
    float max, min, avg, mult, neg1, neg2;
    double n1, n2, power, sqr, sin1, cos1, tan1, sin2, cos2, tan2;
    char s1[20];
    printf("Enter your name: ");
    scanf("%s", s1);
    printf("Enter first number: ");
    scanf("%lf", &n1);
    printf("Enter second number: ");
    scanf("%lf", &n2);
    

    if (n1 > n2)
    {
        max = n1;
    }
    else if (n2 > n1)
    {
        max = n2;
    }


    if (n1 < n2)
    {
        min = n1;
    }
    else if (n2 < n1)
    {
        min = n2;
    }
    

    if (n1 >= 0)
    {
        neg1 = n1 * (-1);
    }
    if (n2 >= 0)
    {
        neg2 = n2 * (-1);
    }


    avg = (n1 + n2) / 2;
    mult = n1 * n2;
    power = pow(n1, n2);
    sqr = sqrt(avg);
    sin1 = sin(n1);
    cos1 = cos(n1);
    tan1 = tan(n1);
    sin2 = sin(n2);
    cos2 = cos(n2);
    tan2 = tan(n2);
    printf("===========================\n");
    printf("Char: %s\n", s1);
    printf("First number: %.2lf\n", n1);
    printf("Second number: %.2lf\n", n2);
    printf("Max value: %.2f\n", max);
    printf("Min value: %.2f\n", min);
    printf("Average value: %.2f\n", avg);
    printf("First number * Second number: %.2f\n", mult);
    printf("First number power Secnod number: %.2lf\n", round(power - ((pow(power, 2)))));
    printf("===========================\n");
    int p1 = n1, p2 = n2;
    if (abs(p1 - p2) <= 50)
    {
        for (int a = n1, b = n2; a <= b; a++)
        {
            printf("I love you\n");
        }
    }
    else
    {
        for (int c = 0, d = 20; c <= d; c++)
        {
            printf("I love you\n");
        }
    }

    printf("\nAll I love is you\n\n");
    printf("===========================\n");
    printf("All number x (-1): %.2f, %.2f\n", neg1, neg2);
    printf("Square root of sum: %.4lf\n", sqr);
    printf("Sin Cos Tan of first number: %.2lf, %.2lf, %.2lf rad\n", sin1, cos1, tan1);
    printf("Sin Cos Tan of second number: %.2lf, %.2lf, %.2lf rad\n", sin2, cos2, tan2);
    printf("Sum / tan of cos and sin: %.2lf\n", avg / tan(cos(avg)/sin(avg)));
    return 0;
}























