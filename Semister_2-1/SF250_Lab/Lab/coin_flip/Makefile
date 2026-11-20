NAME = coin
SRCS = coin.c coin_sim.c coin_print.c
CFLAGS = -Wall -Wextra -O2

$(NAME): $(SRCS) coin.h
	$(CC) $(CFLAGS) $(SRCS) -o $(NAME) -lm

clean:
	rm -f $(NAME)

.PHONY: clean
