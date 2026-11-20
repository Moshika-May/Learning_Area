NAME = bp
SRCS = bp.c bp_math.c bp_print.c
CFLAGS = -Wall -Wextra -O2

$(NAME): $(SRCS) bp.h
	$(CC) $(CFLAGS) $(SRCS) -o $(NAME) -lm

clean:
	rm -f $(NAME)

.PHONY: clean
