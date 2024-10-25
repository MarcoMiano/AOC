# AOC23 D4p2: Scratchcards
import re


class Card(object):
    def __init__(
        self, card_number: int, winning_numbers: list, my_numbers: list
    ) -> None:
        self.number: int = card_number
        self.winning_numbers: list[str] = winning_numbers
        self.my_numbers: list[str] = my_numbers

    def __iter__(self):
        return self

    def __next__(self):
        pass


class Cards(object):
    def __init__(self) -> None:
        self.cards: list = list()
        self.count: int = 0

    def append(self, new_object: Card, qty: int) -> None:
        self.cards.append([new_object, qty])

    def scratch(self) -> None:
        for card, qty in self.cards:
            win = 0
            for number in card.my_numbers:
                if number in card.winning_numbers:
                    win += 1
            for i in range(card.number, card.number + win):
                self.cards[i][1] += qty
        self.__private_count()

    def __private_count(self) -> int:
        for _, qty in self.cards:
            self.count += qty
        return self.count


def parse_input_file(input_file) -> Cards:
    cards = Cards()
    for line in input_file:
        card_number, numbers = line.split(":")

        card_number = re.sub(r"\s+", "", card_number[4::])

        winning_numbers, my_numbers = numbers.split("|")
        winning_numbers = winning_numbers.strip().replace("  ", " ").split(" ")
        my_numbers = my_numbers.strip().replace("  ", " ").split(" ")

        card = Card(int(card_number), winning_numbers, my_numbers)
        cards.append(card, 1)
    return cards


def main() -> None:
    with open("2023//Day4//input.txt") as f:
        input_file = f.read().strip().split("\n")

    cards = parse_input_file(input_file)

    cards.scratch()

    print(cards.count)


if __name__ == "__main__":
    main()
