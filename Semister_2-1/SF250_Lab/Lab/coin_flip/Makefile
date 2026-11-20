NAME = coin_flip
SRCS = coin_flip.c coin_flip_sim.c coin_flip_print.c
CFLAGS = -Wall -Wextra -O2
ARGS = 1000 0.5 42

all: $(NAME)

$(NAME): $(SRCS) coin_flip.h
	$(CC) $(CFLAGS) $(SRCS) -o $(NAME) -lm

# make run               runs the example above
# make run ARGS="..."    runs with your own arguments
run: $(NAME)
	./$(NAME) $(ARGS)

clean:
	rm -f $(NAME)

re: clean all

.PHONY: all run clean re
