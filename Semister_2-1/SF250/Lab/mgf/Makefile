CFLAGS = -O2 -Wall -Wextra -std=c11 -D_GNU_SOURCE
all: mgf_discrete mgf_continuous
%: %.c plot.h
	$(CC) $(CFLAGS) $< -o $@ -lm

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
