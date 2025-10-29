# API Reference

## Core Components

### Main

**Entry point** - Compiles and executes `.fscc` programs

**Workflow:**

1. Reads source file from `sys.argv[1]`
2. Tokenizes input using Lexer
3. Parses tokens into AST
4. Transforms AST for multi-expression expansion
5. Executes the transformed AST

**Returns:** `list` - Flattened execution results

**Raises:**

- `Exception` - No input file specified
- `FileNotFoundError` - Source file not found
- `SyntaxError` - Various syntax errors from compilation stages

### Lexer

**Lexical analyzer** - Converts source code into tokens

**Token Types:**

- **Operators:** `+`, `-`, `*`, `/`, `->`, `(`, `)`, `;`
- **Literals:** integers, floats, strings (single/double quoted)
- **Identifiers:** variable and function names
- **Comments:** `# single-line` and `### block ###`

**Key Methods:**

- `make_tokens()` → `list[Token]` - Main tokenization method
- `make_number()` → `Token` - Parse numeric literals
- `make_string()` → `Token` - Parse strings and identifiers
- `skip_token()` - Handle comments

### Parser

**Recursive-descent parser** - Builds Abstract Syntax Tree from tokens

**AST Node Types:**

- `SCALAR` - Literals and identifiers
- `TASK_NODE` - Prefix operators with operands
- `MULTI_EXPR` - Multiple expressions in parentheses
- `VARIABLE_ASSIGNMENT` - Variable assignments

**Key Methods:**

- `parse()` → `list[Node]` - Top-level parsing
- `parse_expression()` → `Node` - Parse single expression
- `variable_assignment_parser()` → `list[list[Node]]` - Handle assignments

### Transformer

**AST transformer** - Expands multi-expressions and task nodes

**Transformation Logic:**

- Expands `MULTI_EXPR` and `TASK_NODE` children into all combinations
- Processes variable assignments into `[variable, value]` pairs
- Preserves `CALCULATION` nodes during transformation

**Key Methods:**

- `transform(ast)` → `MULTI_EXPR` - Main transformation entry point
- `multi_expression()` - Handle multi-expression expansion
- `variable_assignment_transform()` - Process variable assignments

### Executor

**AST interpreter** - Evaluates transformed AST and produces results

**Features:**

- Arithmetic operations (`+`, `-`, `*`, `/`)
- Variable assignment and scoping
- Built-in function support (e.g., `print`)
- Multi-expression evaluation

**Key Methods:**

- `execute(ast)` → `list` - Main execution method
- `execute_single_command(ast)` → `int | float | list` - Evaluate single node
- `variable_assignment_execute()` - Handle batch assignments
- `execute_arrow()` - Process arrow operations (print/store)

## Built-in Modules

### Operation

**Arithmetic engine** - Performs mathematical operations

**Supported Operations:**

- `+` - Sum all numbers (empty → 0)
- `-` - Subtract sequentially (empty → 0)  
- `*` - Multiply all numbers (empty → 1)
- `/` - Divide sequentially (empty → 0)

**Methods:**

- `calculate(operator, numbers)` → `int | float` - Execute operation

### Environment

**Variable storage** - Manages scoped variable storage

**Scope Support:**

- Global scope by default
- Parent-child scope relationships

**Methods:**
- `add_variable(value, name, parent='global')` - Store variables
- `lookup(variable, parent='global')` → `int | float` - Retrieve variables
