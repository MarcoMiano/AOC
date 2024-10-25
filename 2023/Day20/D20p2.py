# AOC23 D20p2: Pulse Propagation
from collections import Counter, deque
from math import lcm
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


def module_configurator(
    config: list[str],
) -> tuple[dict[str, tuple[CommunicationModule, list[str], bool]], dict[str, int]]:
    def find_inputs(config, label) -> list[str]:
        lines_found = [line.split(" -> ")[0] for line in config if label in line]
        inputs = [mod_lbl[1:] for mod_lbl in lines_found if not label in mod_lbl]
        return inputs

    def find_output_module(modules, config) -> str:
        output_modules = re.findall(r"\b[a-z]+\b", " ".join(config))
        output_modules = Counter(output_modules)
        output_modules = [
            key
            for key, count in output_modules.items()
            if count == 1 and key != "broadcaster"
        ]
        if len(output_modules) > 1:
            raise ValueError(f"Too many output modules found: {output_modules}")
        output_module = "".join(output_modules)
        modules[output_module] = CommunicationModule(output_module), []

        out_mod_feed = list()
        for descriptor in config:
            module, outputs = descriptor.split(" -> ")
            if output_module in outputs:
                out_mod_feed.append(module[1:])

        if len(out_mod_feed) > 1:
            raise ValueError(f"Too many output feeders found: {out_mod_feed}")

        out_mod_feed = out_mod_feed[0]

        return out_mod_feed

    modules: dict[str, tuple[CommunicationModule, list[str], bool]] = dict()

    out_mod_feed = find_output_module(modules, config)

    watchlist: dict[str, int] = dict()

    for descriptor in config:
        module, outputs = descriptor.split(" -> ")
        outputs = outputs.split(", ")
        if module == "broadcaster":
            modules["broadcaster"] = CommunicationModule("broadcaster"), outputs, False
            continue
        if module[0].isalpha():
            raise ValueError(f"Module type of {module} is not allowed")

        type_module = module[0]
        label = module[1:]
        watch = False
        if out_mod_feed in outputs:
            watchlist[label] = 0
            watch = True

        match type_module:
            case "%":
                modules[label] = FlipFlop(label), outputs, watch
            case "&":
                inputs = find_inputs(config, label)
                modules[label] = Conjunction(label, inputs), outputs, watch

    return modules, watchlist


def push_button(
    modules: dict[str, tuple[CommunicationModule, list[str], bool]],
    watchlist: dict[str, int],
    count: int,
) -> None:
    signal_calls = deque()
    for output in modules["broadcaster"][1]:
        signal_calls.append(("broadcaster", output))

    while signal_calls:
        source, destination = signal_calls.popleft()
        pulse = modules[source][0].get_output()
        if pulse and modules[source][2]:
            watchlist[source] = count

        modules[destination][0].process_input(pulse, source)
        if not pulse or isinstance(modules[destination][0], Conjunction):
            for output in modules[destination][1]:
                signal_calls.append((destination, output))
    return


def main() -> None:
    with open("2023//Day20//input.txt") as f:
        config = f.read().strip().splitlines()
    modules, watchlist = module_configurator(config)

    count = 1
    while min(watchlist.values()) == 0:
        push_button(modules, watchlist, count)
        count += 1
    print(lcm(*watchlist.values()))


if __name__ == "__main__":
    main()
