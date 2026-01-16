NAME = libpushswap.a
HEADERS = push_swap.h
CC = cc
CFLAGS = -Wall -Wextra -Werror
EXEC = push_swap
BONUS_EXEC = checker
SRC = ft_assign_index.c ft_checkdup.c ft_checksorted.c ft_check_utils.c\
	  ft_error.c ft_lst_utils2.c ft_lst_utils3.c\
	ft_lst_utils.c ft_operations2.c ft_operations3.c ft_operations.c\
	ft_parsing.c ft_push_swap.c ft_sort_array.c\
	ft_sort_big.c ft_sort_small.c ft_split.c ft_validate_str.c
BONUS_SRC = ft_checker.c ft_checker_utils.c ft_strcmp.c get_next_line.c\
			get_next_line_utils.c
OBJ = $(SRC:.c=.o)
OBJ_BONUS = $(BONUS_SRC:.c=.o)

all: $(EXEC)

$(NAME): $(OBJ)
	ar rcs $(NAME) $(OBJ)

bonus: .bonus

.bonus: $(NAME) $(OBJ_BONUS)
	ar rcs $(NAME) $(OBJ_BONUS)
	$(CC) $(CFLAGS) ft_checker.o $(NAME) -o checker
	@touch .bonus

%.o: %.c $(HEADERS)
	$(CC) $(CFLAGS) -c $< -o $@

$(EXEC): $(NAME) $(OBJ)
	$(CC) $(CFLAGS) ft_push_swap.o $(NAME) -o $(EXEC)

clean:
	rm -f $(OBJ) $(OBJ_BONUS)

fclean: clean
	rm -f $(NAME) $(EXEC) checker

re: fclean all
