CFLAGS = -O2 -Wall -Wextra -std=c11 -D_GNU_SOURCE
DISC = discrete_moment_generating_function
CONT = continuous_moment_generating_function
DISC_SRCS = $(DISC).c discrete_math.c discrete_num.c discrete_out.c \
	discrete_cb.c plot.c
CONT_SRCS = $(CONT).c continuous_math.c continuous_num.c continuous_out.c \
	continuous_cb.c plot.c
ARGS_D = binomial 20 0.4
ARGS_C = gaussian 1 2

all: $(DISC) $(CONT)

$(DISC): $(DISC_SRCS) discrete.h plot.h
	$(CC) $(CFLAGS) $(DISC_SRCS) -o $@ -lm

$(CONT): $(CONT_SRCS) continuous.h plot.h
	$(CC) $(CFLAGS) $(CONT_SRCS) -o $@ -lm

# make run-discrete                          runs the discrete example
# make run-discrete ARGS_D="poisson 4"       runs with your own arguments
# make run-continuous ARGS_C="uniform 0 2"   same for the continuous program
run-discrete: $(DISC)
	./$(DISC) $(ARGS_D)

run-continuous: $(CONT)
	./$(CONT) $(ARGS_C)

run: run-discrete run-continuous

# every distribution, small numbers
test: all
	./$(DISC) bernoulli 0.3
	./$(DISC) binomial 20 0.4
	./$(DISC) poisson 4
	./$(CONT) uniform 0 2
	./$(CONT) exponential 2
	./$(CONT) gaussian 1 2

# stress: huge n / lambda / N
big: all
	./$(DISC) binomial 1000000000 0.3
	./$(DISC) poisson 100000000000
	./$(CONT) gaussian 1 2 20000000

clean:
	rm -f $(DISC) $(CONT)

re: clean all

.PHONY: all run run-discrete run-continuous test big clean re
