# AOC23 D5p1: If You Give A Seed A Fertilizer


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

    def lookup(self, source_id: int) -> int:
        for destination_range_start, source_range_start, range_length in self.table:
            if source_id in range(
                source_range_start, source_range_start + range_length
            ):
                return destination_range_start + (source_id - source_range_start)
        return source_id


class Seed(object):
    def __init__(
        self,
        seed,
        soil=0,
        fertilizer=0,
        water=0,
        light=0,
        temperature=0,
        humidity=0,
        location=0,
    ) -> None:
        self.seed = seed
        self.soil = soil
        self.fertilizer = fertilizer
        self.water = water
        self.light = light
        self.temperature = temperature
        self.humidity = humidity
        self.location = location

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
        self.soil = seed_to_soil.lookup(self.seed)
        self.fertilizer = soil_to_fertilizer.lookup(self.soil)
        self.water = fertilizer_to_water.lookup(self.fertilizer)
        self.light = water_to_light.lookup(self.water)
        self.temperature = light_to_temperature.lookup(self.light)
        self.humidity = temperature_to_humidity.lookup(self.temperature)
        self.location = humidity_to_location.lookup(self.humidity)


def main() -> None:
    with open("Day5\\input.txt") as f:
        input_file = f.read().strip().split("\n")

    seeds: list[Seed] = list()

    seed_to_soil = Map()
    soil_to_fertilizer = Map()
    fertilizer_to_water = Map()
    water_to_light = Map()
    light_to_temperature = Map()
    temperature_to_humidity = Map()
    humidity_to_location = Map()

    for line_number, line in enumerate(input_file):
        if line.find("seeds: ") >= 0:
            for seed_num in line[6::].strip().split(" "):
                seeds.append(Seed(int(seed_num)))
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
        locations.append(seed.location)

    print(min(locations))


if __name__ == "__main__":
    main()
