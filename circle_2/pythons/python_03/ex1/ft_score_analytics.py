import sys

def main():
    print("=== Player Score Analytics ===")
    arguments = sys.argv
    length = len(arguments)
    if length < 2:
        print("No scores provided. Usage: python3 ", end="")
        print("ft_score_analytics.py <score1> <score2> ...")
        return

    i = 1
    nums = []
    try:
        while i < length:
            nums.append(int(arguments[i]))
            i += 1

    except:
        print("oops, I typed ’banana’ instead of ’1000’")
        return

    print(f"Scores processed: {nums}")
    print(f"Total players: {length - 1}")
    print(f"Total score: {sum(nums)}")
    print(f"Average score: {sum(nums) / len(nums)}")
    print(f"High score: {max(nums)}")
    print(f"Low score: {min(nums)}")
    print(f"Score range: {max(nums) - min(nums)}\n")


main()
