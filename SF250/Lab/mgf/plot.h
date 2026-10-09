/* tiny ASCII plotter shared by both programs */
#include <math.h>
#include <stdio.h>
#include <string.h>

static void plot(const char *title, double (*f)(double), double lo, double hi) {
    enum { W = 70, H = 16 };
    double y[W], ymin = INFINITY, ymax = -INFINITY;
    char g[H][W + 1];
    for (int i = 0; i < W; i++) {
        y[i] = f(lo + (hi - lo) * i / (W - 1));
        if (isfinite(y[i])) { ymin = fmin(ymin, y[i]); ymax = fmax(ymax, y[i]); }
    }
    if (!(ymax > ymin)) ymax = ymin + 1;
    memset(g, ' ', sizeof g);
    for (int r = 0; r < H; r++) g[r][W] = 0;
    for (int i = 0; i < W; i++)
        if (isfinite(y[i])) g[(int)((ymax - y[i]) / (ymax - ymin) * (H - 1) + .5)][i] = '*';
    printf("\n%s\n", title);
    for (int r = 0; r < H; r++) printf("%11.4g |%s\n", ymax - (ymax - ymin) * r / (H - 1), g[r]);
    printf("%11s +%.*s\n%11s  %-*.4g%.4g\n", "", W, "----------------------------------------------------------------------", "", W - 8, lo, hi);
}
