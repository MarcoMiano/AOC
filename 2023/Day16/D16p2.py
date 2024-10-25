# AOC23 D16p2: The Floor Will Be Lava
import multiprocessing as mp


def trace_beam(
    contraption: list[str],
    seen: set[tuple[int, int, str]],
    start_pos: tuple[int, int] = (0, 0),
    start_direction: str = "r",
) -> list[list[bool]]:
    rows = len(contraption)
    columns = len(contraption[0])
    heatmap = [[False for _ in range(columns)] for _ in range(rows)]

    end = False
    r, c = start_pos
    d = start_direction
    contraption = contraption
    while not end:
        if not (0 <= r < rows) or not (0 <= c < columns):
            break
        if (r, c, d) in seen:
            break

        match char := contraption[r][c]:
            case ".":
                heatmap[r][c] = True
                seen.add((r, c, d))
                if d == "r" and c + 1 < columns:
                    c += 1
                elif d == "d" and r + 1 < rows:
                    r += 1
                elif d == "l" and c - 1 >= 0:
                    c -= 1
                elif d == "u" and r - 1 >= 0:
                    r -= 1
                else:
                    if not d in "rdlu":
                        raise ValueError(
                            f"The direction: {d} is Invalid. Possible values are r: Right, d: Down, l:Left, u: Up."
                        )
                    end = True
            case "/":
                heatmap[r][c] = True
                if d == "r" and r - 1 >= 0:
                    r -= 1
                    d = "u"
                elif d == "d" and c - 1 >= 0:
                    c -= 1
                    d = "l"
                elif d == "l" and r + 1 < rows:
                    r += 1
                    d = "d"
                elif d == "u" and c + 1 < columns:
                    c += 1
                    d = "r"
                else:
                    if not d in "rdlu":
                        raise ValueError(
                            f"The direction: {d} is Invalid. Possible values are r: Right, d: Down, l:Left, u: Up."
                        )
                    end = True
            case "\\":
                heatmap[r][c] = True
                if d == "r" and r + 1 < columns:
                    r += 1
                    d = "d"
                elif d == "d" and c + 1 < columns:
                    c += 1
                    d = "r"
                elif d == "l" and r - 1 >= 0:
                    r -= 1
                    d = "u"
                elif d == "u" and c - 1 >= 0:
                    c -= 1
                    d = "l"
                else:
                    if not d in "rdlu":
                        raise ValueError(
                            f"The direction: {d} is Invalid. Possible values are r: Right, d: Down, l:Left, u: Up."
                        )
                    end = True
            case "|":
                heatmap[r][c] = True
                if d == "r" or d == "l":
                    if r - 1 >= 0 and r + 1 < rows:
                        heatmap = list_or(
                            heatmap, trace_beam(contraption, seen, (r - 1, c), "u")
                        )
                        r += 1
                        d = "d"
                    elif not r - 1 >= 0 and r + 1 < rows:
                        r += 1
                        d = "d"
                    elif r - 1 >= 0 and not r + 1 < rows:
                        r -= 1
                        d = "u"
                    else:
                        end = True
                elif d == "d" and r + 1 < rows:
                    r += 1
                elif d == "u" and r - 1 >= 0:
                    r -= 1
                else:
                    if not d in "rdlu":
                        raise ValueError(
                            f"The direction: {d} is Invalid. Possible values are r: Right, d: Down, l:Left, u: Up."
                        )
                    end = True
            case "-":
                heatmap[r][c] = True
                if d == "u" or d == "d":
                    if c - 1 >= 0 and c + 1 < columns:
                        heatmap = list_or(
                            heatmap, trace_beam(contraption, seen, (r, c - 1), "l")
                        )
                        c += 1
                        d = "r"
                    elif not c - 1 >= 0 and c + 1 < columns:
                        c += 1
                        d = "r"
                    elif c - 1 >= 0 and not c + 1 < columns:
                        c -= 1
                        d = "l"
                    else:
                        end = True
                elif d == "r" and c + 1 < rows:
                    c += 1
                elif d == "l" and c - 1 >= 0:
                    c -= 1
                else:
                    if not d in "rdlu":
                        raise ValueError(
                            f"The direction: {d} is Invalid. Possible values are r: Right, d: Down, l:Left, u: Up."
                        )
                    end = True
            case _:
                raise ValueError(
                    f"Found character: {char} is Invalid. Possbile values are . \\ / | -"
                )

    return heatmap


def get_energized_tiles(
    queue,
    contraption: list[str],
    seen: set[tuple[int, int, str]],
    start_pos: tuple[int, int] = (0, 0),
    start_direction: str = "r",
) -> None:
    output = 0
    heatmap = trace_beam(contraption, seen, start_pos, start_direction)
    for row in heatmap:
        for tile in row:
            output += 1 if tile else 0
    queue.put(output)


def list_or(list1: list[list[bool]], list2: list[list[bool]]) -> list[list[bool]]:
    list3 = [[False for _ in range(len(list2[0]))] for _ in range(len(list2))]
    for r, (row1, row2) in enumerate(zip(list1, list2)):
        for i, (item1, item2) in enumerate(zip(row1, row2)):
            list3[r][i] = item1 or item2

    return list3


def print_heatmap(heatmap: list[list[bool]]) -> None:
    for row in heatmap:
        rowc = ""
        for tile in row:
            rowc += "#" if tile else "."
        print(rowc)


def main() -> None:
    with open("Day16\\input.txt") as f:
        contraption = f.read().strip().splitlines()
    rows = len(contraption)
    columns = len(contraption[0])
    max_count = 0

    process_list = []
    queue = mp.Queue()
    for r in range(rows):
        p = mp.Process(
            target=get_energized_tiles,
            args=(queue, contraption, set(), (r, 0), "r"),
        )
        p.start()
        process_list.append(p)
        p = mp.Process(
            target=get_energized_tiles,
            args=(queue, contraption, set(), (r, columns - 1), "l"),
        )
        p.start()
        process_list.append(p)

    for c in range(columns):
        p = mp.Process(
            target=get_energized_tiles,
            args=(queue, contraption, set(), (0, c), "d"),
        )
        p.start()
        process_list.append(p)
        p = mp.Process(
            target=get_energized_tiles,
            args=(queue, contraption, set(), (rows - 1, c), "u"),
        )
        p.start()
        process_list.append(p)

    for p in process_list:
        p.join()

    max_count = queue.get() if not queue.empty() else 0

    while not queue.empty():
        max_count = max(max_count, queue.get())
    print(max_count)


if __name__ == "__main__":
    main()
