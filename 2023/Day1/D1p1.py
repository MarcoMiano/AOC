# AOC23 D1p1: Trebuchet?!
import re

answer = 0

with open("./input.txt", "r") as input:
    for line in input:
        first_digit = re.search(r"\d", line).group()
        last_digit = re.search(r"\d", line[::-1]).group()
        print(first_digit + last_digit)
        answer += int(first_digit + last_digit)

print(answer)
