NAME = clt
SRCS = clt.c clt_sim.c clt_print.c
CFLAGS = -Wall -Wextra -O2

$(NAME): $(SRCS) clt.h
	$(CC) $(CFLAGS) $(SRCS) -o $(NAME) -lm

clean:
	rm -f $(NAME)

.PHONY: clean
