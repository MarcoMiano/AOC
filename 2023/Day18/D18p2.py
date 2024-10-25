# AOC23 D18p2: Lavaduct Lagoon


DIR = {"R": (1, 0), "D": (0, 1), "L": (-1, 0), "U": (0, -1)}


def convert_dig_plan(wrong_dig_plan: list[str]) -> list[str]:
    dir_enc = {0: "R", 1: "D", 2: "L", 3: "U"}
    dig_plan: list[str] = []
    for line in wrong_dig_plan:
        _, _, raw_instruction = line.split()
        magnitude = int(raw_instruction[2:-2], 16)
        direction = dir_enc[int(raw_instruction[-2])]
        dig_plan.append(f"{direction} {magnitude}")

    return dig_plan


def get_vertices_perimeter(dig_plan: list[str]) -> tuple[list[tuple[int, int]], int]:
    vertices: list[tuple[int, int]] = [(0, 0)]
    perimeter = 0
    for line in dig_plan:
        direction, magnitude = line.split()
        magnitude = int(magnitude)
        perimeter += magnitude

        new_x = vertices[-1][0] + DIR[direction][0] * magnitude
        new_y = vertices[-1][1] + DIR[direction][1] * magnitude

        vertices.append((new_x, new_y))

    return vertices, perimeter


def get_internal_area(vertices: list[tuple[int, int]]) -> int:
    d_area = 0
    for i in range(len(vertices)):
        d_area += vertices[i][1] * (
            vertices[i - 1][0] - vertices[(i + 1) % len(vertices)][0]
        )
    d_area = abs(d_area)

    return d_area // 2


def main() -> None:
    with open("Day18\\input-sm.txt") as f:
        dig_plan = f.read().strip().splitlines()

    dig_plan = convert_dig_plan(dig_plan)

    vertices, perimeter = get_vertices_perimeter(dig_plan)

    lagoon_volume = (get_internal_area(vertices) - perimeter // 2 + 1) + perimeter
    print(lagoon_volume)


if __name__ == "__main__":
    main()
