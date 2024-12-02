def fibonacci_recursive(n: int) -> int:

    if not isinstance(n, int) or n < 0:
        raise ValueError("il numero deve essere un intero positivo")


    if n == 0:
        return 0
    elif n == 1:
        return 1

    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def sum_of_digits_recursive(num: int) -> int:

    num=abs(num)

    if num < 10:
        return num

    return num % 10 + sum_of_digits_recursive(num // 10)


def is_palindrome_number(num: int) -> bool:

    num_str = str(num)
    return num_str == num_str[::-1]