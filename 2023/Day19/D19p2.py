# AOC23 D19p1: Aplenty
# Thanks to jmerle https://github.com/jmerle/advent-of-code-2023/blob/master/src/day19/part2.py
from math import prod


def main() -> None:
    with open("2023//Day19//input.txt") as f:
        sections = f.read().strip().split("\n\n")

    workflows = {}
    for line in sections[0].split("\n"):
        id, steps = line.split("{")
        workflows[id] = []

        for step in steps[:-1].split(","):
            done = False

            for ch in "xmas":
                for op in "<>":
                    if step.startswith(ch + op):
                        value = int(step[2:].split(":")[0])
                        nxt = step.split(":")[1]
                        workflows[id].append((ch, op, value, nxt))
                        done = True

            if not done:
                workflows[id].append((step,))

    queue = [("in", 0, {ch: (1, 4000) for ch in "xmas"})]
    t = 0

    while len(queue) > 0:
        workflow, idx, bounds = queue.pop()

        if workflow == "A":
            t += prod(bounds[ch][1] - bounds[ch][0] + 1 for ch in "xmas")

        if workflow in "AR" or idx >= len(workflows[workflow]):
            continue

        step = workflows[workflow][idx]

        if len(step) == 4 and step[1] == "<":
            iff = bounds.copy()
            els = bounds

            iff[step[0]] = (iff[step[0]][0], step[2] - 1)
            els[step[0]] = (step[2], els[step[0]][1])

            queue.append((step[3], 0, iff))
            queue.append((workflow, idx + 1, els))
        elif len(step) == 4 and step[1] == ">":
            iff = bounds.copy()
            els = bounds

            iff[step[0]] = (step[2] + 1, iff[step[0]][1])
            els[step[0]] = (els[step[0]][0], step[2])

            queue.append((step[3], 0, iff))
            queue.append((workflow, idx + 1, els))
        elif len(step) == 1:
            queue.append((step[0], 0, bounds))

    print(t)


if __name__ == "__main__":
    main()
