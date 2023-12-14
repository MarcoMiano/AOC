# AOC23 D9p1: Mirage Maintenance


def reduce(sequence: list[int], past_sequence=[]) -> list | int:
    new_sequence = []
    is_first = True if not past_sequence else False

    for i in range(sequence.__len__() - 1):
        new_sequence.append(sequence[i + 1] - sequence[i])

    past_sequence.append(sequence[-1])

    if all(number == 0 for number in new_sequence):
        return past_sequence

    output_sequence = reduce(new_sequence, past_sequence)

    if is_first:
        return sum(output_sequence)

    return output_sequence


def main() -> None:
    with open("Day9\\input.txt") as f:
        input_file = f.read().strip().split("\n")

    answer = 0

    for line in input_file:
        str_sequence = line.split()
        sequence = [int(numbers) for numbers in str_sequence]

        step = reduce(sequence, [])

        answer += step

    print(answer)


if __name__ == "__main__":
    main()
