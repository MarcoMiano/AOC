# AOC23 D18p1: Lavaduct Lagoon


def shoelace(vertices: list) -> float:
    area = 0
    if len(vertices) <= 2:
        return area

    d_area = 0

    current_point = vertices.pop()
    while vertices:
        next_point = vertices.pop()
        d_area += abs(
            (current_point[0] * next_point[1]) - (current_point[1] * next_point[0])
        )

        current_point = next_point

    area = d_area // 2

    return area


def main() -> None:
    with open("Day18\\input.txt") as f:
        dig_plan = f.read().strip().splitlines()

    vertices: list[tuple[int, int]] = [(0, 0)]
    perimeter = 0

    for line in dig_plan:
        direction, magnitude, color = line.split()
        magnitude = int(magnitude) - 1
        perimeter += magnitude

        match direction:
            case "R":
                new_x = vertices[-1][0] + magnitude
                new_y = vertices[-1][1]
            case "D":
                new_x = vertices[-1][0]
                new_y = vertices[-1][1] + magnitude
            case "L":
                new_x = vertices[-1][0] - magnitude
                new_y = vertices[-1][1]
            case "U":
                new_x = vertices[-1][0]
                new_y = vertices[-1][1] - magnitude
            case _:
                raise ValueError("Invalid direction")

        vertices.append((new_x, new_y))

    area = shoelace(vertices) + perimeter + 1

    print(area)


if __name__ == "__main__":
    main()
