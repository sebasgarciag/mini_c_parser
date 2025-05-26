# Mini C Parser

A complete syntax analyzer (parser) for a Mini C programming language that reads tokens and generates an Abstract Syntax Tree (AST).

## Quick Start

```bash
# Run a simple demo
python mini_c_parser.py

# Run all tests
python tests.py
```

## Features

✅ **Lexical Analysis** - Tokenizes Mini C source code  
✅ **Syntax Analysis** - Builds AST using recursive descent parsing  
✅ **Error Handling** - Detailed error messages with line/column info  
✅ **Pretty Printing** - Visual tree representation of AST  
✅ **Operator Precedence** - Correct handling of arithmetic operators  

## Supported Language

```c
// Variable declarations
int x;
int y;

// Assignments with expressions
x = 5;
y = x + 3 * (2 - 1);
```

## Files

- `mini_c_parser.py` - Main implementation with lexer, parser, and AST classes (heavily commented)
- `tests.py` - All tests for the parser (9 clear test cases)
- `user_manual.md` - Comprehensive documentation and usage guide
- `README.md` - This file

## Example Output

```
Program
├── VariableDeclaration (type: int, name: x)
├── Assignment
│   ├── Variable (name: x)
│   └── BinaryOperation (operator: +)
│       ├── Number (value: 3)
│       └── Number (value: 5)
```

## Grammar

```
Program ::= { Declaration | Assignment }
Declaration ::= 'int' IDENTIFIER ';'
Assignment ::= IDENTIFIER '=' Expression ';'
Expression ::= Term { ('+' | '-') Term }
Term ::= Factor { ('*' | '/') Factor }
Factor ::= NUMBER | IDENTIFIER | '(' Expression ')'
```

For detailed documentation, see `user_manual.md`. 