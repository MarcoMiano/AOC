# AOC23 D5p2: If You Give A Seed A Fertilizer


class Map(object):
    def __init__(self) -> None:
        self.table: list = list()
        # table = {source, destination}

    def resolve_map(
        self, destination_range_start, source_range_start, range_length
    ) -> None:
        for i in range(range_length):
            self.table[source_range_start + i] = destination_range_start + i

    def parse_strings(self, input_file: list[str], line_number: int) -> None:
        i = line_number + 1
        while input_file[i] != "":
            destination_range_start, source_range_start, range_length = (
                input_file[i].strip().split(" ")
            )
            self.table.append(
                (
                    int(destination_range_start),
                    int(source_range_start),
                    int(range_length),
                )
            )
            i += 1
            if i >= len(input_file):
                break

    def lookup(self, source_pair: list[int]) -> int:
        remaining_pair = source_pair
        results = list()

        while remaining_pair:
            current_pair = remaining_pair.pop()
            for destination_range_start, source_range_start, range_length in self.table:
                if (
                    current_pair[1] < source_range_start
                    or source_range_start + range_length <= current_pair[0]
                ):
                    continue
                elif (
                    source_range_start
                    <= current_pair[0]
                    <= current_pair[1]
                    < source_range_start + range_length
                ):
                    offset = current_pair[0] - source_range_start
                    results.append(
                        (
                            destination_range_start + offset,
                            destination_range_start
                            + offset
                            + current_pair[1]
                            - current_pair[0],
                        )
                    )
                    break
                elif (
                    current_pair[0]
                    < source_range_start
                    <= current_pair[1]
                    < source_range_start + range_length
                ):
                    offset = current_pair[1] - source_range_start
                    results.append(
                        (destination_range_start, destination_range_start + offset)
                    )
                    remaining_pair.append((current_pair[0], source_range_start - 1))
                    break
                elif (
                    source_range_start
                    <= current_pair[0]
                    < source_range_start + range_length
                    <= current_pair[1]
                ):
                    offset = current_pair[0] - source_range_start
                    results.append(
                        (
                            destination_range_start + offset,
                            destination_range_start + range_length - 1,
                        )
                    )
                    remaining_pair.append(
                        (source_range_start + range_length, current_pair[1])
                    )
                    break
                elif (
                    current_pair[0]
                    < source_range_start
                    <= source_range_start + range_length
                    <= current_pair[1]
                ):
                    results.append(
                        (
                            destination_range_start,
                            destination_range_start + range_length - 1,
                        )
                    )
                    remaining_pair.append((current_pair[0], source_range_start - 1))
                    remaining_pair.append(
                        (source_range_start + range_length, current_pair[1])
                    )
                    break
            else:
                results.append(current_pair)
        return results


class Seed(object):
    def __init__(self, seed_pair: list[int]) -> None:
        self.seed_pair = seed_pair

    def cultivate(
        self,
        seed_to_soil: Map,
        soil_to_fertilizer: Map,
        fertilizer_to_water: Map,
        water_to_light: Map,
        light_to_temperature: Map,
        temperature_to_humidity: Map,
        humidity_to_location: Map,
    ) -> int:
        self.soil = seed_to_soil.lookup(self.seed_pair)
        self.fertilizer = soil_to_fertilizer.lookup(self.soil)
        self.water = fertilizer_to_water.lookup(self.fertilizer)
        self.light = water_to_light.lookup(self.water)
        self.temperature = light_to_temperature.lookup(self.light)
        self.humidity = temperature_to_humidity.lookup(self.temperature)
        self.location = humidity_to_location.lookup(self.humidity)


def main() -> None:
    with open("2023//Day5//input.txt") as f:
        input_file = f.read().strip().split("\n")

    seeds = list()

    seed_to_soil = Map()
    soil_to_fertilizer = Map()
    fertilizer_to_water = Map()
    water_to_light = Map()
    light_to_temperature = Map()
    temperature_to_humidity = Map()
    humidity_to_location = Map()

    for line_number, line in enumerate(input_file):
        if line.find("seeds: ") >= 0:
            seed_raw_list = line[6::].strip().split(" ")
            seed_raw_list = [int(x) for x in seed_raw_list]
            for i in range(0, len(seed_raw_list), 2):
                seeds.append(
                    Seed([[seed_raw_list[i], seed_raw_list[i] + seed_raw_list[i + 1]]])
                )

        elif line == "seed-to-soil map:":
            seed_to_soil.parse_strings(input_file, line_number)
        elif line == "soil-to-fertilizer map:":
            soil_to_fertilizer.parse_strings(input_file, line_number)
        elif line == "fertilizer-to-water map:":
            fertilizer_to_water.parse_strings(input_file, line_number)
        elif line == "water-to-light map:":
            water_to_light.parse_strings(input_file, line_number)
        elif line == "light-to-temperature map:":
            light_to_temperature.parse_strings(input_file, line_number)
        elif line == "temperature-to-humidity map:":
            temperature_to_humidity.parse_strings(input_file, line_number)
        elif line == "humidity-to-location map:":
            humidity_to_location.parse_strings(input_file, line_number)
        else:
            continue

    locations = list()

    for seed in seeds:
        seed.cultivate(
            seed_to_soil,
            soil_to_fertilizer,
            fertilizer_to_water,
            water_to_light,
            light_to_temperature,
            temperature_to_humidity,
            humidity_to_location,
        )
        locations.extend(seed.location)
    print(min(min(locations)))


if __name__ == "__main__":
    main()
