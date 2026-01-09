import re


def validate_input_nums(s: str, x: int) -> bool:
    pattern = re.compile(r'^\s*\d+(?:\s*,\s*\d+)*\s*$')
    if not pattern.fullmatch(s):
        return False
    try:
        nums = [int(n.strip()) for n in s.split(',')]
    except ValueError:
        return False
    return all(1 <= n <= x for n in nums)
