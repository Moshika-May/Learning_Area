NAME = waiting_times
SRCS = waiting_times.c
CFLAGS = -Wall -Wextra -O2
INPUT = 15\n100000\n

all: $(NAME)

$(NAME): $(SRCS)
	$(CC) $(CFLAGS) $(SRCS) -o $(NAME) -lm

# The program asks two questions (average interval T, number of samples).
# make run                         answers 15 and 100000
# make run INPUT='10\n5000\n'      answers with your own numbers
run: $(NAME)
	printf '$(INPUT)' | ./$(NAME)

clean:
	rm -f $(NAME)

re: clean all

.PHONY: all run clean re
