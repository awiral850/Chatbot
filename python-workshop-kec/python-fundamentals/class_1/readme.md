# Python Fundamentals: A Comprehensive Guide for Beginners

## 1. Data Types & Structures in Depth

Understanding how to store and access data is the foundation of programming.

### Lists (Mutable Sequence)
An ordered collection of items. You can change it after creation.

#### Common List Methods
Here are some useful built-in methods for lists:

```python
nums = [10, 20, 30]
nums.append(40)      # Adds 40 to the end: [10, 20, 30, 40]
nums.pop()          # Removes and returns last item: 40
nums.insert(1, 15)  # Inserts 15 at index 1: [10, 15, 20, 30]
nums.remove(20)     # Removes first occurrence of 20
nums.extend([50, 60]) # Adds multiple items: [10, 15, 30, 50, 60]
nums.sort()         # Sorts the list in place
nums.reverse()      # Reverses the list in place
print(nums.index(15)) # Returns index of first occurrence of 15
print(nums.count(10)) # Counts occurrences of 10
```

#### Looping Through a List
You can loop through a list using a `for` loop:
```python
fruits = ["Apple", "Banana", "Cherry"]
for fruit in fruits:
    print(fruit)
# Output:
# Apple
# Banana
# Cherry
```

**1. Accessing Data:**
Lists uses "Zero-based indexing".
```python
fruits = ["Apple", "Banana", "Cherry", "Date", "Elderberry"]

print(fruits[0])      # "Apple" (First item)
print(fruits[2])      # "Cherry"
print(fruits[-1])     # "Elderberry" (Last item, negative index counts from back)

# Slicing [start:end] (end is exclusive)
print(fruits[1:3])    # ["Banana", "Cherry"]
```

**2. Modifying Data:**
```python
fruits[0] = "Apricot" # Change value at index 0
fruits.append("Fig")  # Add to the end
fruits.insert(1, "Blueberry") # Insert at specific index
print(fruits)
```

### Dictionaries (Key-Value Mapping)
Unordered collection storing data in `key: value` pairs. Keys must be unique and immutable (usually strings).

#### Common Dictionary Methods
Here are some useful built-in methods for dictionaries:

```python
person = {"name": "Alex", "age": 25}
person.get("age")         # Returns value for 'age', or None if missing
person.keys()              # Returns all keys
person.values()            # Returns all values
person.items()             # Returns list of (key, value) pairs
person.update({"city": "KTM"}) # Adds/updates key-value pairs
person.pop("age")         # Removes key 'age' and returns its value
person.setdefault("gender", "M") # Adds key 'gender' with value 'M' if not present
person.clear()             # Removes all items from dictionary
```

#### Looping Through a Dictionary
You can loop through keys, values, or both:
```python
person = {"name": "Alex", "age": 25, "city": "KTM"}
# Loop through keys
for key in person:
    print(key)
# Loop through values
for value in person.values():
    print(value)
# Loop through key-value pairs
for key, value in person.items():
    print(f"{key}: {value}")
```

**1. Accessing Data:**
```python
user = {
    "name": "Jane", 
    "role": "Admin", 
    "score": 85
}

print(user["name"])   # "Jane"
# print(user["age"])  # CRASH! KeyError because "age" doesn't exist

# The Safer Way: .get()
print(user.get("age"))        # None (No crash)
print(user.get("age", 18))    # 18 (Default value if missing)
```

**2. Modifying Data:**
```python
user["score"] = 90        # Update existing key
user["city"] = "Pokhara"  # Add new key-value pair
```

### Immutable Types (Tuples) & Sets
*   **Tuple**: Like a list, but cannot be changed. Used for fixed data (e.g., coordinates).
    *   `coords = (10.5, 20.1)`
*   **Set**: Unordered collection of **unique** items. Great for removing duplicates.
    *   `unique_ids = {1, 2, 2, 3}  # Becomes {1, 2, 3}`

### Immutability and Reassignment vs Mutation
**Immutable types** (like `int`, `float`, `str`, `tuple`) cannot be changed after creation. If you "change" their value, you are actually creating a new object and reassigning the variable to point to it.

```python
a = 2         # 'a' points to memory address X (value 2)
a = 4         # 'a' now points to memory address Y (value 4)
# This is NOT mutation. The value 2 is not changed to 4. 'a' just points to a new object.

my_tuple = (1, 2, 3)
# my_tuple[0] = 10  # ERROR! Tuples cannot be changed.
```

**Mutable types** (like `list`, `dict`, `set`) can be changed in-place:
```python
my_list = [1, 2, 3]
my_list[0] = 10   # Changes the value inside the same list object
```

---

## 2. Functions: The Building Blocks

A function is a reusable block of code that performs a specific task.

### Why do we need functions?
It's not just about reusing code. It's about **Logical Segregation**.

1.  **Reusability**: Write once, use many times.
2.  **Abstraction**: Hiding complex details. You don't need to know *how* `print()` works to use it.
3.  **Organization (Step-down logic)**: Even if a code block runs only **ONCE**, putting it in a function makes the main program readable. Instead of 50 lines of math, you see `calculate_salary()`.

### Indentation Matters
Python uses whitespace (indentation) to know what code belongs inside the function.

```python
def my_function():
    print("Inside function")
    print("Still inside")
print("Outside function") # This runs after function definition is done
```

### Defining and Invoking Functions
To define a function, use the `def` keyword. To run (invoke) it, use its name followed by parentheses:
```python
def greet(name):
    print(f"Hello, {name}!")

greet("Saksham")  # Function invocation
```

### A "Realistic" Example
Business Logic: Apply a discount, then add tax.

```python
def calculate_final_bill(price, discount_percent, tax_percent):
    # Step 1: Calculate Discount
    discount_amount = price * (discount_percent / 100)
    price_after_discount = price - discount_amount
    
    # Step 2: Calculate Tax on discounted price
    tax_amount = price_after_discount * (tax_percent / 100)
    
    # Step 3: Final Total
    total = price_after_discount + tax_amount
    
    return total

# Usage
laptop_final = calculate_final_bill(100000, 10, 13) # 10% off, then 13% Tax
print(f"Final Bill: {laptop_final}")
```

**Note : Function name cannot be same as variable name**

---

## 3. File Handling in Detail

To work with files, we need to understand **Modes**.

### File Modes
*   `'r'`: **Read** (Default). Error if file missing.
*   `'w'`: **Write**. Creates new file or **TRUNCATES** (clears) existing file.
*   `'a'`: **Append**. Adds to end of file.
*   `'b'`: **Binary**. For images, audio, etc. (e.g., `'rb'`, `'wb'`).
*   `'r+'`: Read and Write.

#### Examples for Each Mode
```python
# 'r' - Read mode
with open("example.txt", "r") as f:
    content = f.read()

# 'w' - Write mode (overwrites file)
with open("example.txt", "w") as f:
    f.write("This will overwrite the file.")

# 'a' - Append mode
with open("example.txt", "a") as f:
    f.write("This will add to the end of the file.\n")

# 'b' - Binary mode (read)
with open("image.png", "rb") as f:
    data = f.read()

# 'wb' - Binary mode (write)
with open("image_copy.png", "wb") as f:
    f.write(data)

# 'r+' - Read and Write mode
with open("example.txt", "r+") as f:
    old = f.read()
    f.write("Adding new content while keeping old.")
```

### The `write` rule
File's `.write()` method ONLY accepts **strings**. You cannot pass an integer or list directly.

```python
with open("score.txt", "w") as f:
    # f.write(100) # TypeError!
    f.write("100") # Correct
```

### Reading Strategies

#### 1. Load Entire File Into Memory
This reads the whole file at once. Use only for small/medium files.
```python
with open("large_log.txt", "r") as f:
    content = f.read()
    print(content)
```

#### 2. Read Line by Line (Memory Efficient)
Best for large text files.
```python
with open("large_log.txt", "r") as f:
    for line in f:
        print(line.strip())
```

#### 3. Read Chunk by Chunk (Binary or Large Files)
Useful for images, videos, or very large files.
```python
chunk_size = 4096 # 4KB
with open("video.mp4", "rb") as f:
    while (chunk := f.read(chunk_size)):
        process_video_frame(chunk)
```

---

## 4. JSON Handling: The Bridge

JSON (JavaScript Object Notation) is the standard format for data exchange. 

**Key Concept**:
*   Python **Dict** <--> **JSON String** <--> **File**

### The 4 Functions
1.  `json.dumps(dict)` -> Returns a **String** (Serialization).
2.  `json.loads(string)` -> Returns a **Dict**.
3.  `json.dump(dict, file)` -> Writes directly to **File**.
4.  `json.load(file)` -> Reads directly from **File**.

### Why `dumps` before write?
Since file `write()` only accepts strings, we must convert our dictionary to a string first.

**Method A: Manual String Writing (dumps)**
```python
import json

user_data = {"id": 1, "active": True}

# Convert dict to string
json_string = json.dumps(user_data) 

with open("user.json", "w") as f:
    f.write(json_string) # Writing the string
```

**Method B: Direct File Writing (dump)**
Does the conversion and writing in one step.
```python
with open("user.json", "w") as f:
    json.dump(user_data, f, indent=4)
```

---

## Writing and Reading List of Dicts Line by Line (JSON Lines)

Sometimes, you want to store each dictionary on a separate line in a file (JSON Lines format). This is useful for large datasets or streaming data.

### Writing List of Dicts Line by Line
```python
import json

data = [
    {"id": 1, "name": "Ram"},
    {"id": 2, "name": "Sita"},
    {"id": 3, "name": "Hari"}
]

with open("users.jsonl", "w") as f:
    for item in data:
        f.write(json.dumps(item) + "\n")  # Write each dict as a JSON string, one per line
```

### Reading List of Dicts Line by Line
```python
import json

result = []
with open("users.jsonl", "r") as f:
    for line in f:
        result.append(json.loads(line))  # Convert each line back to dict and append to list

print(result)
# Output: [{'id': 1, 'name': 'Ram'}, {'id': 2, 'name': 'Sita'}, {'id': 3, 'name': 'Hari'}]
```

### Reading from a JSON File
To read data from a JSON file and convert it back to a Python dictionary:
```python
import json

with open("user.json", "r") as f:
    data = json.load(f)
    print(data)  # Output: {'id': 1, 'active': True}
    print(data["id"])  # Accessing value by key
```

---

## 5. Loops in Python
Loops let you repeat actions. The two main types are:

### For Loop
Use a `for` loop when you know how many times you want to repeat, or when iterating over a collection (list, dict, etc).

**Iterating over a list:**
```python
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)
```

**Using range:**
```python
for i in range(5):  # 0, 1, 2, 3, 4
    print(i)
```

### While Loop
Use a `while` loop when you want to repeat until a condition changes (often for user input, or when you don't know how many times in advance).

**Typical use: user-driven menu or input**
```python
while True:
    cmd = input("Type 'exit' to quit: ")
    if cmd == "exit":
        break
    print(f"You typed: {cmd}")
```

**When to use which?**
- Use `for` when iterating over a sequence or a fixed number of times.
- Use `while` when looping until a condition is met (unknown number of times, e.g., user input, waiting for a signal).

---

## 6. Conditional Statements & Walrus Operator
Conditionals let you run code only if something is true:

```python
age = 18
if age >= 18:
    print("Adult")
else:
    print("Minor")
```

### Walrus Operator (`:=`)
The walrus operator lets you assign and check a value in a single line (Python 3.8+). It's useful when you want to use a value immediately after getting it, especially in loops or conditionals.

**Without walrus:**
```python
value = my_dict.get("key")
if value is not None:
    print(value)
```
**With walrus:**
```python
if (value := my_dict.get("key")) is not None:
    print(value)
```

**When to use?**
- Use the walrus operator when you want to both assign and check a value in a single statement, to avoid repeating work or variable names.
- Especially handy in loops that read input or data until a condition is met.

---

## 7. Operators in Python
Operators let you perform calculations and comparisons:

**Arithmetic:** `+`, `-`, `*`, `/`, `//` (floor), `%` (modulo), `**` (power)
```python
result = 5 + 3 * 2  # 11
```
**Comparison:** `==`, `!=`, `<`, `>`, `<=`, `>=`
```python
print(5 > 3)  # True
```
**Logical:** `and`, `or`, `not`
```python
print(True and False)  # False
```

**Identity vs Equality:**
- `==` checks if values are equal.
- `is` checks if two variables point to the same object in memory.

```python
x = [1, 2, 3]
y = [1, 2, 3]
z = x
print(x == y)  # True (values are equal)
print(x is y)  # False (different objects)
print(x is z)  # True (same object)
```

**Other niche behaviors:**
- Chained comparisons: `1 < x < 10`
- `in` operator: `if 2 in [1,2,3]: ...`
- Augmented assignment: `x += 1`
