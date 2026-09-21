NAME = codexion

CC = cc
CFLAGS = -Wall -Wextra -Werror -pthread

SRCS = \
	coders/main.c \
	coders/init.c \
	coders/parse.c \
	coders/parse_utils.c \
	coders/simulation.c \
	coders/simulation_utils.c \
	coders/coder.c \
	coders/coder_init.c \
	coders/coder_utils.c \
	coders/dongle.c \
	coders/dongle_utils.c \
	coders/monitor.c \
	coders/monitor_wait.c \
	coders/logger.c \
	coders/scheduler.c \
	coders/scheduler_utils.c \
	coders/scheduler_heap.c \
	coders/scheduler_runtime.c \
	coders/scheduler_guard.c \
	coders/cleanup.c

OBJS = $(SRCS:.c=.o)

RM = rm -f

all: $(NAME)

$(NAME): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $(NAME)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	$(RM) $(OBJS)

fclean: clean
	$(RM) $(NAME)

re: fclean all

.PHONY: all clean fclean re
