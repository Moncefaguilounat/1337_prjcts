
import sys

print("=== Command Quest ===")

arguments = sys.argv
length = len(arguments)
if length < 2:
    print("No arguments provided!")
    print(f"Program name: {sys.argv[0]}")

else:
    print(f"Program name: {sys.argv[0]}")
    print(f"Arguments recieved: {length - 1}")
    i = 1
    while i < length:
        print(f"Argument {i}: {arguments[i]}")
        i += 1

print(f"Total arguments: {length}")
