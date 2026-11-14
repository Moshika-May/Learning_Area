// Waiting times: regular buses (uniform [0,T]) vs random buses (exponential, mean T)
// build: gcc waiting_times.c -o waiting_times -lm
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define BINS 30   // bin width = T/10, covers [0,3T); last bin also holds the overflow

static double u(void) { return (rand() + 1.0) / (RAND_MAX + 2.0); } // (0,1)

static void hist(const char *name, const int *h, double w, double mean) {
    int max = 1;
    for (int i = 0; i < BINS; i++) if (h[i] > max) max = h[i];
    printf("\n%s  (mean = %.3f)\n", name, mean);
    for (int i = 0; i < BINS; i++) {
        printf("%6.2f-%6.2f |", i * w, (i + 1) * w);
        for (int j = 0; j < h[i] * 50 / max; j++) putchar('#');
        printf(" %d\n", h[i]);
    }
}

int main(void) {
    double T;
    int n;
    printf("Average bus interval T (minutes, e.g. 15): ");
    if (scanf("%lf", &T) != 1 || T <= 0) return 1;
    printf("Number of samples (e.g. 100000): ");
    if (scanf("%d", &n) != 1 || n <= 0) return 1;

    int reg[BINS] = {0}, rnd[BINS] = {0};
    double sr = 0, se = 0, w = T / 10;
    srand(250);
    for (int i = 0; i < n; i++) {
        double a = T * u(), b = -T * log(u());   // uniform / exponential wait
        sr += a; se += b;
        int ia = (int)(a / w), ib = (int)(b / w);
        reg[ia < BINS ? ia : BINS - 1]++;
        rnd[ib < BINS ? ib : BINS - 1]++;
    }
    hist("1) Regular buses: Uniform[0,T]", reg, w, sr / n);
    printf("   theory T/2 = %.3f\n", T / 2);
    hist("2) Random buses: Exponential(1/T)", rnd, w, se / n);
    printf("   theory T = %.3f   (last bar includes waits >= 3T)\n", T);
    return 0;
}
