👉🏾 Initial Generated Code:
```python
def process_data(numbers, mode='average'):
    if not numbers:
        return 0
    if mode == 'sum':
        return sum(numbers)
    elif mode == 'average':
        return sum(numbers) / len(numbers)
    else:
        raise ValueError("Invalid mode. Choose 'sum' or 'average'.")
```

➡️  Test results: 5 passed, 7 failed

Failed Test Cases:
Test #5
  Inputs: ([], 'sum')
  Expected: None
  Actual: 0
Test #6
  Inputs: ([1, 3, 4], 'median')
  Expected: 3
  Error: Invalid mode. Choose 'sum' or 'average'.
Test #7
  Inputs: ([1, 2, 3, 5], 'median')
  Expected: 2.5
  Error: Invalid mode. Choose 'sum' or 'average'.
Test #8
  Inputs: ([1, 2, 'a', 3], 'sum')
  Expected: 6
  Error: unsupported operand type(s) for +: 'int' and 'str'
Test #9
  Inputs: ([1, 2, None, 3, 'b', 4], 'average')
  Expected: 2.5
  Error: unsupported operand type(s) for +: 'int' and 'NoneType'
Test #10
  Inputs: ([10], 'median')
  Expected: 10
  Error: Invalid mode. Choose 'sum' or 'average'.
Test #11
  Inputs: ([], 'median')
  Expected: None
  Actual: 0


👉🏾 Improved Code (Loop #1):
```python
def process_data(numbers, mode='average'):
    if not numbers:
        return None

    # Filter out invalid entries for sum and average calculations
    valid_numbers = [num for num in numbers if isinstance(num, (int, float))]
    
    if mode == 'sum':
        return sum(valid_numbers)
    elif mode == 'average':
        if not valid_numbers:
            return None
        return sum(valid_numbers) / len(valid_numbers)
    elif mode == 'median':
        sorted_numbers = sorted(valid_numbers)
        n = len(sorted_numbers)
        if n == 0:
            return None
        mid = n // 2
        if n % 2 == 0:
            return (sorted_numbers[mid - 1] + sorted_numbers[mid]) / 2
        else:
            return sorted_numbers[mid]
    else:
        raise ValueError("Invalid mode. Choose 'sum', 'average', or 'median'.")
```

➡️  Test results: 12 passed, 0 failed


Success! All tests passed ✅