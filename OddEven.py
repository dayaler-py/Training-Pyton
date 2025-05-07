def count_even_odd(numbers):
    even_count = sum(1 for num in numbers if num % 2 == 0)
    odd_count = len(numbers) - even_count
    return even_count, odd_count

s_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even, odd = count_even_odd(s_numbers)
print(f"In the list {s_numbers}, there are {even} even numbers and {odd} odd numbers.")