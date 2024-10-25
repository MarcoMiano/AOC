# AOC23 D9p2: Mirage Maintenance


def reduce(sequence: list[int], past_sequence=[]) -> list[int]:
    new_sequence = []
    is_first = True if not past_sequence else False

    for i in range(sequence.__len__() - 1):
        new_sequence.append(sequence[i + 1] - sequence[i])

    past_sequence.insert(0, sequence[0])

    if all(number == 0 for number in new_sequence):
        return past_sequence

    output_sequence = reduce(new_sequence, past_sequence)

    if is_first:
        output = 0
        for i in range(output_sequence.__len__()):
            output = output_sequence[i] - output

        return [output]

    return output_sequence


def main() -> None:
    with open("2023//Day9//input.txt") as f:
        input_file = f.read().strip().split("\n")

    answer = 0

    for line in input_file:
        str_sequence = line.split()
        sequence = [int(numbers) for numbers in str_sequence]

        step = reduce(sequence, [])[0]
        answer += step

    print(answer)


if __name__ == "__main__":
    main()
