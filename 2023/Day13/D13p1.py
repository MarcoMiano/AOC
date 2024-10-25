# AOC23 D13p1: Point of Incidence
from collections import deque


def get_reflection_score(pattern: list[str], vertical: bool = False) -> int:
    if vertical:
        pattern = list(zip(*pattern[::-1]))
        pattern = ["".join(line) for line in pattern]

    output = int()

    for l, line in enumerate(
        pattern
    ):  # Iterate the pattern per line having also the line index
        if (
            l + 1 > len(pattern) - 1
        ):  # If the next line index is over the lenght of the pattern exit
            break

        if line == pattern[l + 1]:  # If the current line and the next one are the same
            i = 1

            while (
                l - i >= 0 and l + i < len(pattern) - 1
            ):  # Trace back and check the previous line (l - i) and the next line (l + i + 1)
                if (
                    pattern[l - i] != pattern[l + i + 1]
                ):  # If the new lines aren't the same then the reflection is broken
                    break
                i += 1
            else:  # If the trace back and expansion finish with a reflection return the correct score
                if vertical:
                    output = l + 1
                else:
                    output = (
                        l + 1
                    ) * 100  # If the reflection is horrizontal multiply the score by 100
                break
    return output


def get_reflections_sum(patterns: list[list[str]]) -> int:
    reflections_sum = 0

    for p, pattern in enumerate(
        patterns
    ):  # For every pattern find the vertical or the horizzontal reflection score
        reflections_sum += get_reflection_score(pattern)
        reflections_sum += get_reflection_score(pattern, vertical=True)

    return reflections_sum


def main() -> None:
    with open("2023//Day13//input.txt") as f:
        input_file = deque(f.read().strip().splitlines())

    patterns: list[list[str]] = [[]]
    pattern_counter = 0

    while input_file:
        line = input_file.popleft()

        if line == "":
            pattern_counter += 1
            patterns.append([])
        else:
            patterns[pattern_counter].append(line)

    answer = get_reflections_sum(patterns)

    print(answer)

    return


if __name__ == "__main__":
    main()
