/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mouaguil <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/10 18:39:49 by mouaguil          #+#    #+#             */
/*   Updated: 2026/01/10 18:39:51 by mouaguil         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef PUSH_SWAP_H
# define PUSH_SWAP_H

# include <stdlib.h>
# include <unistd.h>

typedef struct s_stack
{
	int				nbr;
	int				index;
	struct s_stack	*next;
}	t_stack;

int		ft_lstsize(t_stack *lst);
void	ft_lstclear(t_stack **lst);
void	ft_lstadd_back(t_stack **lst, t_stack *new);
void	ft_freestr(char **lst);
void	ft_lst_stack(t_stack **a, int n);
t_stack	*ft_parsing(int ac, char **av);
t_stack	*ft_lstnew(int *content);
t_stack	*ft_lstlast(t_stack *lst);
void	ft_error(void);
void	ft_sa(t_stack **a, int print);
void	ft_sb(t_stack **b, int print);
void	ft_ss(t_stack **a, t_stack **b, int print);
void	ft_pa(t_stack **a, t_stack **b, int print);
void	ft_pb(t_stack **a, t_stack **b, int print);
void	ft_ra(t_stack **a, int print);
void	ft_rb(t_stack **b, int print);
void	ft_rr(t_stack **a, t_stack **b, int print);
void	ft_rra(t_stack **a, int print);
void	ft_rrb(t_stack **b, int print);
void	ft_rrr(t_stack **a, t_stack **b, int print);
void	ft_sort_array(int *tab, int size);
void	ft_assign_index(t_stack *a);
int		ft_checksorted(t_stack *a);
int		ft_max_index(t_stack *s);
int		ft_min_index(t_stack *s);
int		ft_find_position(t_stack *s, int index);
int		ft_min(t_stack *lst);
int		ft_max(t_stack *lst);
int		ft_find_index(t_stack *s, int n);
int		ft_checkdup(t_stack *a, int n);
int		ft_isdigit(int c);
int		ft_just_spaces(char *s);
void	ft_sort_array(int *tab, int size);
void	ft_sort_five(t_stack **a, t_stack **b);
void	ft_sort_four(t_stack **a, t_stack **b);
void	ft_sort_three(t_stack **a);
void	ft_sort_two(t_stack **a);
void	ft_big_sort(t_stack **a, t_stack **b);
int		ft_validate_str(const char *str, int *flag);
char	**ft_split(char const *s);

# ifndef BUFFER_SIZE
#  define BUFFER_SIZE 42
# endif

char	*get_next_line(int fd);

size_t	ft_strlen(const char *s);
char	*ft_strchr(const char *s, int c);
char	*ft_strdup(const char *s);
char	*ft_strjoin(char const *s1, char const *s2);
char	*ft_substr(char const *s, unsigned int start, size_t len);
void	ok_ko(int f);
int		final_check(t_stack *a, t_stack *b);
void	apply_instr(char *instr, t_stack **a, t_stack **b);
void	clear_and_error(char *instr, t_stack **a, t_stack **b);
int		validate_instruction(char *instruction);
int		ft_strcmp(const char *s1, const char *s2);

#endif
