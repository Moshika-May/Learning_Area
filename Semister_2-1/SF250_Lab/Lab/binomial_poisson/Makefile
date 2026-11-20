NAME = binomial_poisson
SRCS = binomial_poisson.c binomial_poisson_math.c binomial_poisson_print.c
CFLAGS = -Wall -Wextra -O2
ARGS = 100 0.05 100000 1

all: $(NAME)

$(NAME): $(SRCS) binomial_poisson.h
	$(CC) $(CFLAGS) $(SRCS) -o $(NAME) -lm

# make run               runs the example above
# make run ARGS="..."    runs with your own arguments
run: $(NAME)
	./$(NAME) $(ARGS)

clean:
	rm -f $(NAME)

re: clean all

.PHONY: all run clean re
