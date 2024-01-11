# AOC23 D20p1: Pulse Propagation
from collections import Counter, deque
import re


class CommunicationModule(object):
    def __init__(self, label) -> None:
        self.state: bool = False
        self.label: str = label

    def process_input(self, input_state, _) -> None:
        self.state = input_state

    def get_output(self) -> bool:
        return self.state


class FlipFlop(CommunicationModule):
    def process_input(self, input_state, _) -> None:
        self.state = self.state == input_state


class Conjunction(CommunicationModule):
    def __init__(self, label, inputs) -> None:
        super().__init__(label)
        self.state = True
        self.inputs = {key: False for key in inputs}

    def process_input(self, input_state, input_name) -> None:
        self.inputs[input_name] = input_state
        self.state = not all(self.inputs.values())


def find_inputs(config: list[str], label: str) -> list[str]:
    lines_found = [line.split(" -> ")[0] for line in config if label in line]
    inputs = [mod_lbl[1:] for mod_lbl in lines_found if not label in mod_lbl]
    return inputs


def module_configurator(
    config: list[str],
) -> dict[str, tuple[CommunicationModule, list[str]]]:
    modules: dict[str, tuple[CommunicationModule, list[str]]] = dict()

    for descriptor in config:
        module, outputs = descriptor.split(" -> ")
        if "%" in module:
            modules[module[1:]] = FlipFlop(module[1:]), outputs.split(", ")
        elif "&" in module:
            inputs = find_inputs(config, module[1:])
            modules[module[1:]] = Conjunction(module[1:], inputs), outputs.split(", ")
        elif module == "broadcaster":
            modules["broadcaster"] = CommunicationModule("broadcaster"), outputs.split(
                ", "
            )
        else:
            raise ValueError(f"Module type of {module} is not allowed")

    output_modules = re.findall(r"\b[a-z]+\b", " ".join(config))
    output_modules = Counter(output_modules)
    output_modules = [
        key
        for key, count in output_modules.items()
        if count == 1 and key != "broadcaster"
    ]

    for label in output_modules:
        modules[label] = CommunicationModule(label), []

    return modules


def get_current_states(
    modules: dict[str, tuple[CommunicationModule, list[str]]]
) -> set[tuple[str, bool]]:
    states = set()
    for module in modules.values():
        if module[0].label == "output":
            continue
        states.add((module[0].label, module[0].state))

    return states


def execute_queue(
    modules: dict[str, tuple[CommunicationModule, list[str]]]
) -> tuple[int, int]:
    low_signal_count = 1
    high_signal_count = 0
    signal_calls = deque()
    for output in modules["broadcaster"][1]:
        signal_calls.append(("broadcaster", output))

    while signal_calls:
        source, destination = signal_calls.popleft()
        pulse = modules[source][0].get_output()

        modules[destination][0].process_input(pulse, source)
        if not pulse or isinstance(modules[destination][0], Conjunction):
            for output in modules[destination][1]:
                # print(f"append: {destination}, {output}")
                signal_calls.append((destination, output))

        if pulse:
            high_signal_count += 1
        else:
            low_signal_count += 1
    return low_signal_count, high_signal_count


def main() -> None:
    with open("Day20\\input.txt") as f:
        config = f.read().strip().splitlines()
    modules = module_configurator(config)

    low_signal_count = 0
    high_signal_count = 0

    for _ in range(1000):
        ls, hs = execute_queue(modules)
        low_signal_count += ls
        high_signal_count += hs

    print(int(low_signal_count * high_signal_count))


if __name__ == "__main__":
    main()
