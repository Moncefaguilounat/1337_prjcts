*This project has been created as part of the 42 curriculum by mouaguil.*

# push_swap

## Description
**push_swap** is an algorithmic project whose goal is to sort a list of integers using two stacks and a restricted set of operations.

The program receives a list of integers as arguments and outputs a sequence of instructions that, when applied to the stacks, sorts the numbers in ascending order.  
The challenge of this project lies not only in achieving correct sorting, but in doing so with **the smallest possible number of operations**.

A companion program, **checker**, is used to verify whether a given sequence of instructions correctly sorts the input.

---

## Instructions

### Compilation

To compile the project, run:

```bash
make
#This will generate the executable:
./push_swap

#To compile the bonus checker:
make bonus
#This will generate:
./checker

#To clean object files:
make clean

#To remove all compiled files:
make fclean

#To recompile everything:
make re
```
## Usage
push_swap
./push_swap <list_of_integers>

Example:
./push_swap 3 2 1
The program prints a list of instructions (one per line) that sorts the stack.

## checker
./checker <list_of_integers>

The checker reads instructions from standard input and prints:
OK if the stack is sorted correctly
KO if it is not
Error if an invalid instruction is encountered

## Features & Technical Choices
### Input validation:

Non-numeric arguments
Integer overflow / underflow
Duplicate values
Optimized sorting strategies:
Dedicated logic for small stacks
Indexing (normalization) to simplify comparisons
Efficient stack operations using a linked-list structure
Careful memory management to avoid leaks
Robust handling of edge cases (already sorted input, empty instruction list, EOF cases)

## References

42 Subject PDF: push_swap

Sorting algorithms:
Medium
GeeksforGeeks

## Use of AI
AI tools were used as a learning and reasoning aid during the development of this project.
Specifically, AI was used to:
Clarify algorithmic concepts and complexity trade-offs
Reason about edge cases and undefined behaviors
Review logic for stack operations and input validation
Improve understanding of get_next_line behavior in the context of checker
