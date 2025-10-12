# FlowScript (FS) - The Concise Calculus programming language

### FlowScript (FS) is a Hyper-Concise and Dataflow-Oriented language, born from the "frustration" of repetitive operations in imperative programming.

## Features

- **Dataflow Paradigm**: Natural expression of data transformations
- **Hyper-Concise Syntax**: Minimal boilerplate, maximum expressiveness  
- **Simple Execution Model**: Clear data flow from input to output
- **Arithmetic Operations**: Full support for mathematical expressions
- **Nested Expressions**: Complex computations with clean syntax

## Installation

```bash
git clone https://github.com/qdyg-vn/FlowScript.git
cd FlowScript
# Pure Python - no external dependencies
```

## Usage

```bash
python main.py
```

****

## Example Session:

**Input**: +(1, 2)

**Output**: 3

**Input**: *(+(1, 2), 3)

**Output**: 9

**Input**: /(10, 2)

**Output** 5.0

## Syntax

**+(a, b)**

**-(a, b,*(c, d))**

****

## Core Components

**1.** Lexer - Tokenization

Converts source code to tokens

Recognizes: numbers, operators, parentheses

**2.** Parser - AST Construction

Builds Abstract Syntax Tree using recursive descent

Handles nested expressions naturally

**3.** Executor - Dataflow Execution

Evaluates expressions in dataflow order

Applies operations as data becomes available

## Philosophy

FlowScript eliminates imperative boilerplate by making dataflow the primary concern. 
Instead of worrying about variables and assignment, you focus on how data transforms through operations.
