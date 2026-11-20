NAME = central_limit_theorem
SRCS = central_limit_theorem.c central_limit_theorem_sim.c central_limit_theorem_print.c
CFLAGS = -Wall -Wextra -O2
ARGS = exp 30 10000 1

all: $(NAME)

$(NAME): $(SRCS) central_limit_theorem.h
	$(CC) $(CFLAGS) $(SRCS) -o $(NAME) -lm

# make run               runs the example above
# make run ARGS="..."    runs with your own arguments
run: $(NAME)
	./$(NAME) $(ARGS)

clean:
	rm -f $(NAME)

re: clean all

.PHONY: all run clean re
