# AOC23 D22p1: Sand Slabs


def main() -> None:
    with open("Day22\\input-sm.txt") as f:
        snapshot = f.read().strip().splitlines()
    bricks: list[tuple[tuple[int, ...], int, int]] = list()

    for i, line in enumerate(snapshot):
        coord1s, coord2s = line.split("~")
        coord1: tuple[int, ...] = tuple(int(coord) for coord in coord1s.split(","))
        coord2: tuple[int, ...] = tuple(int(coord) for coord in coord2s.split(","))

        ax = 0
        length = 0
        for ax in range(3):
            if coord1[ax] != coord2[ax]:
                length = abs(coord1[ax] - coord2[ax])
                break
        bricks.append((coord1 if coord1[2] <= coord2[2] else coord2, ax, length))

    bricks = sorted(bricks, key=lambda x: x[0][2])
    print(bricks)
    stabilized_bricks = list()
    for i, brick in enumerate(bricks):
        coord, axis, length = brick
        if coord[2] == 1:
            stabilized_bricks.append(brick)
            continue
        if not stabilized_bricks:
            new_brick = ((*coord[:-1], 1), *brick[1:])
            stabilized_bricks.append(new_brick)
        else:
            for ax in range(3):
                if axis == 0:
                    ...

    # print(stabilized_bricks)


if __name__ == "__main__":
    main()
