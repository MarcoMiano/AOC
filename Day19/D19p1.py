# AOC23 D19p1: Aplenty
from collections import deque


def parse_file(input_file: list[str]) -> tuple[dict[str, tuple], list]:
    raw_workflows, raw_parts = [section.splitlines() for section in input_file]

    workflows = dict()
    parts = list()

    for workflow in raw_workflows:
        name, rules = workflow.split("{")
        rules = rules[:-1].split(",")
        workflows[name] = tuple([rule for rule in rules])

    for part in raw_parts:
        ratings = part[1:-1].split(",")
        part = {rating[0]: int(rating[2:]) for rating in ratings}
        parts.append(part)

    return workflows, parts


def execute_workflows(workflows: dict[str, tuple], part: dict) -> bool:
    def execute_workflow(workflow_t: tuple, part: dict) -> str:
        workflow = deque(workflow_t)
        while workflow:
            raw_curr_inst = workflow.popleft()
            if "<" in raw_curr_inst or ">" in raw_curr_inst:
                rating_cat = raw_curr_inst[0]
                operator = raw_curr_inst[1]
                rating_value, next_operation = raw_curr_inst[2:].split(":")
                if eval(f"{part[rating_cat]} {operator} {rating_value}"):
                    return next_operation
                else:
                    continue
            else:
                return raw_curr_inst
        return ""

    end = False
    workflow_name = "in"
    while not end:
        workflow_name = execute_workflow(workflows[workflow_name], part)
        if workflow_name in "AR":
            end = True

    return True if workflow_name == "A" else False


def main() -> None:
    with open("Day19\\input.txt") as f:
        input_file = f.read().strip().split("\n\n")

    workflows, parts = parse_file(input_file)
    ratings_sum = 0

    for part in parts:
        if execute_workflows(workflows, part):
            ratings_sum += sum(part.values())

    print(ratings_sum)


if __name__ == "__main__":
    main()
