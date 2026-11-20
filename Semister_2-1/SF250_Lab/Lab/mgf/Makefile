CFLAGS = -O2 -Wall -Wextra -std=c11 -D_GNU_SOURCE
DISC = mgf_discrete.c dist_math.c dist_num.c dist_cb.c dist_out.c plot.c
CONT = mgf_continuous.c cont_math.c cont_num.c cont_cb.c cont_out.c plot.c

all: mgf_discrete mgf_continuous

mgf_discrete: $(DISC) dist.h plot.h
	$(CC) $(CFLAGS) $(DISC) -o $@ -lm

mgf_continuous: $(CONT) cont.h plot.h
	$(CC) $(CFLAGS) $(CONT) -o $@ -lm

# every distribution, small numbers
test: all
	./mgf_discrete bernoulli 0.3
	./mgf_discrete binomial 20 0.4
	./mgf_discrete poisson 4
	./mgf_continuous uniform 0 2
	./mgf_continuous exponential 2
	./mgf_continuous gaussian 1 2

# stress: huge n / lambda / N
big: all
	./mgf_discrete binomial 1000000000 0.3
	./mgf_discrete poisson 100000000000
	./mgf_continuous gaussian 1 2 20000000

clean:
	rm -f mgf_discrete mgf_continuous

.PHONY: all test big clean
