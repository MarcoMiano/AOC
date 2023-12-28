# AOC23 D13p1: Point of Incidence

from collections import deque
from pprint import pprint


def clean_smudge(line1: str, line2: str) -> bool:
    diff_count = 0

    for ch1, ch2 in zip(line1, line2):
        if ch1 != ch2:
            diff_count += 1

    if diff_count == 0:
        raise RuntimeError(f"Lines are the same, nothing to clean. {line1} == {line2}")

    elif diff_count > 1:
        return False

    return True


def get_reflection_score(
    pattern: list[str], vertical: bool = False
) -> tuple[int, bool]:
    if vertical:
        pattern = list(zip(*pattern[::-1]))
        pattern = ["".join(line) for line in pattern]

    output = (0, False)

    def get_reflection_score_inner(pattern_inner: list[str], l_inner: int):
        output_inner = int()
        cleaned = False
        print("Found possible reflection")
        i = 1
        while l_inner - i >= 0 and l_inner + i < len(pattern_inner) - 1:
            print(
                f"{pattern_inner[l_inner - i]} == {pattern_inner[l_inner + i + 1]} : {pattern_inner[l_inner - i] == pattern_inner[l_inner + i + 1]}"
            )
            if (
                pattern_inner[l_inner - i] != pattern_inner[l_inner + i + 1]
                and not cleaned
            ):
                print("Attempting to clean smudge.")
                cleaned = clean_smudge(
                    pattern_inner[l_inner - i], pattern_inner[l_inner + i + 1]
                )
                if cleaned:
                    print("Possible smudge cleaned, considering this lines as good.")
                    i += 1
                    continue
                break
            elif (
                pattern_inner[l_inner - i] != pattern_inner[l_inner + i + 1] and cleaned
            ):
                break
            i += 1
        else:
            print("Found reflection returning score")
            if vertical:
                output_inner = l_inner + 1
            else:
                output_inner = (l_inner + 1) * 100
        return output_inner, cleaned

    for l, line in enumerate(pattern):
        if l + 1 > len(pattern) - 1:
            break
        print(f"line: {line}, next_line: {pattern[l + 1]}")

        if line != pattern[l + 1] and clean_smudge(line, pattern[l + 1]):
            output = get_reflection_score_inner(pattern, l)

        if line == pattern[l + 1]:
            output = get_reflection_score_inner(pattern, l)

    return output


def get_reflections_sum(patterns: list[list[str]]) -> int:
    reflections_score_sum = 0

    for p, pattern in enumerate(patterns):
        print(f"pattern id: {p}")
        pprint(pattern)
        print("\n")

        reflection_score_h, cleaned_h = get_reflection_score(pattern)
        print(f"reflection_score_h: {reflection_score_h}, cleaned: {cleaned_h}")
        if reflection_score_h != 0 and cleaned_h:
            reflections_score_sum += reflection_score_h
            continue
        reflection_score_v, cleaned_v = get_reflection_score(pattern, vertical=True)
        print(f"reflection_score_v: {reflection_score_v}, cleaned: {cleaned_v}")
        if reflection_score_v != 0 and cleaned_v:
            reflections_score_sum += reflection_score_v
            continue
        reflections_score_sum += reflection_score_h + reflection_score_v

    return reflections_score_sum


def main() -> None:
    with open("Day13\\input-sm.txt") as f:
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
