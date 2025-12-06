def max_joltage(bank: str, count=2) -> str:
    if count == 1:
        return max(bank)

    first = max(bank[: -(count - 1)])

    i = bank.index(first)
    next = max_joltage(bank[i + 1 :], count - 1)
    return first + next


def solution(input_file):
    exact_two = 0
    exact_twelve = 0

    with open(input_file) as f:
        banks = f.read().splitlines()

        for bank in banks:
            exact_two += int(max_joltage(bank, 2))
            exact_twelve += int(max_joltage(bank, 12))

    return exact_two, exact_twelve
