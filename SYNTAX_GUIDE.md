# FlowScript Syntax Guide

## Arithmetic Operations

### Basic Operations

```fscc
+(a, b)    # Addition: a + b
-(a, b)    # Subtraction: a - b  
*(a, b)    # Multiplication: a * b
/(a, b)    # Division: a / b
```

#### Examples:

```fscc
+(2, 3)        # 2 + 3 = 5
/(+(6, 2), 4)  # (6 + 2) / 4 = 2.0
```

### Multiple Operations with Semicolon

Execute multiple calculations with the same operator using `;` as separator:

```fscc
+(a, b; c, d)    # Multiple additions
-(a, b; c, d)    # Multiple subtractions  
*(a, b; c, d)    # Multiple multiplications
/(a, b; c, d)    # Multiple divisions
```

#### Examples:

```fscc
+(2, 3; 4, 6)                    # → 5, 10
/(+(6, 2; 9, 7), -(5, 1; 4, 5))  # → 2.0, -8.0, 4.0, -16.0
```

**Explanation:** The second example generates all combinations:

* `(6 + 2) / (5 - 1)` = 2.0

* `(6 + 2) / (4 - 5)` = -8.0

* `(9 + 7) / (5 - 1)` = 4.0

* `(9 + 7) / (4 - 5)` = -16.0

## Variable Assignment

### Single Assignment

**Use `->` to assign results to variables:** expression -> variable

#### Examples:

```fscc
+(2, 3) -> a        # a = 5
True -> d           # d = True  
None -> e           # e = None
```

## Multiple Assignment

**Assign multiple values to multiple variables:** value1, value2, value3 -> var1, var2, var3

#### Example:

```fscc
0, True, False -> c, d, e  # c=0, d=True, e=False
```

## Output and Printing

### Direct Printing

Print values directly using `-> print`:

expression -> print

value -> print

#### Examples:

```fscc
0 -> print                    # Output: 0
+(1, 2) -> print             # Output: 3
```

### Print with Intermediate Variables

**Chain assignments with printing:** expression -> variable -> print

#### Example:

```fscc
+(1, 2 -> a -> print)  # a = 3, then print(a) → Output: 3
```

## Advanced Examples

### Complex Expression with Variables

```fscc
+(2, 3 -> x) -> print        # x=5, print 5
*(x, 2 -> y) -> print        # y=10, print 10  
/(y, x -> z -> print)        # z=2.0, print 2.0
```

### Batch Operations with Variables

```fscc
+(1, 2; 3, 4 -> results) -> print  # results=[3, 7], print both
```

## Key Features Summary

* Prefix Notation: All operations use `operator(operands)` syntax

* Multiple Execution: Semicolon `;` enables batch operations

* Flexible Assignment: Arrow `->` chains values to variables

* Built-in Printing: Direct output with `-> print`

* Type Support: Numbers, booleans, None values