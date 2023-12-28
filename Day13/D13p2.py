# AOC23 D13p1: Point of Incidence
from calendar import different_locale
from collections import deque
from pprint import pprint


def get_reflection(pattern: list[str]) -> int:
    for l, line in enumerate(pattern):
        if l + 1 > len(pattern) - 1:
            break

        if line == pattern[l + 1]:
            i = 1

            while l - i >= 0 and l + i < len(pattern) - 1:
                if pattern[l - i] != pattern[l + i + 1]:
                    break
                i += 1
            else:
                return l + 1
    return 0


def count_different_chars(line1: str, line2: str) -> int:
    diff_count = 0
    for ch1, ch2 in zip(line1, line2):
        if ch1 != ch2:
            diff_count += 1

    return diff_count


def get_reflection_score(
    pattern: list[str], vertical: bool = False
) -> tuple[int, bool]:
    possible_smudges: list[tuple[int, int]] = list()
    output: int = int()

    def gps_first_layer() -> list[tuple[int, int]]:
        for l, line in enumerate(pattern):
            if l + 1 > len(pattern) - 1:
                break

            if (
                line != pattern[l + 1]
                and count_different_chars(line, pattern[l + 1]) == 1
            ):
                possible_smudges.append((l, l + 1))
        return possible_smudges

    def gps_second_layer():
        possible_smudges1: list[tuple[int, int]] = list()
        for l, line in enumerate(pattern):
            if l + 1 > len(pattern) - 1:
                break

            if line == pattern[l + 1]:
                i = 1
                while l - i >= 0 and l + i < len(pattern) - 1:
                    diff_char = count_different_chars(
                        pattern[l - i], pattern[l + i + 1]
                    )
                    if (
                        pattern[l - i] != pattern[l + i + 1]
                        and diff_char != 1
                        and not possible_smudges1
                    ):
                        break

                    if pattern[l - i] != pattern[l + i + 1] and possible_smudges1:
                        possible_smudges1.pop()
                        break

                    if (
                        pattern[l - i] != pattern[l + i + 1]
                        and diff_char == 1
                        and not possible_smudges1
                    ):
                        possible_smudges1.append((l - i, l + i + 1))
                        i += 1
                        continue

                    i += 1
                else:
                    return l + 1

        return 0

    #   get possible smudges in first layer
    #   verify every possible layer 1 smudges for reflections
    #   if one is found return the score of the one found
    #   if none are found then get possible smudges in second layer and verify them
    #       if one is found and verified return the score of that one
    #   if none are found return 0

    if vertical:
        pattern = list(zip(*pattern[::-1]))
        pattern = ["".join(line) for line in pattern]

    print("Calling gps_first_layer")
    possible_smudges = gps_first_layer()
    print(f"gps_first_layer returned: {possible_smudges}")
    if possible_smudges:
        print("\tChecking all possible smudges.")
        for possible_smudge in possible_smudges:
            new_pattern = pattern
            new_pattern[possible_smudge[0]] = new_pattern[possible_smudge[1]]
            output = get_reflection(new_pattern)
            if output:
                print(
                    f"\tFound reflection, returning: {output if vertical else (output) * 100}"
                )
                return output if vertical else (output) * 100, True

    print("Calling gps_second_layer")
    output = gps_second_layer()
    print(f"gps_second_layer returned: {output}")
    if output:
        print(f"Found reflection, returning: {output if vertical else (output) * 100}")
        return output if vertical else (output) * 100, True

    print("No smudge found, calling get_reflection")
    output = get_reflection(pattern)
    print(f"get_reflection returned: {output}")
    print(f"Returning: {output if vertical else (output) * 100}")
    return output if vertical else (output) * 100, False


def get_reflections_sum(patterns: list[list[str]]) -> int:
    reflections_sum = 0

    for p, pattern in enumerate(patterns):
        print(f"\npattern id: {p}")
        print(f"Pattern:")
        pprint(pattern)
        print("\nCalling get_reflection_score HORIZONTAL")
        reflections_sum_h, cleaned_h = get_reflection_score(pattern)
        print(f"get_reflection_score HORIZONTAL returned: {reflections_sum_h}")

        if cleaned_h:
            reflections_sum += reflections_sum_h
            continue

        print("Calling get_reflection_score VERTICAL")
        reflections_sum_v, cleaned_v = get_reflection_score(pattern, vertical=True)
        print(f"get_reflection_score VERTICAL returned: {reflections_sum_v}")

        if cleaned_v:
            reflections_sum += reflections_sum_v
            continue

        reflections_sum += reflections_sum_h + reflections_sum_v

    return reflections_sum


def main() -> None:
    with open("Day13\\input.txt") as f:
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
