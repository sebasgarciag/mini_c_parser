# Mini C Parser User Manual

## Overview

The Mini C Parser is a complete syntax analyzer for a simplified C-like programming language. It reads source code, tokenizes it, and generates an Abstract Syntax Tree (AST) that represents the program's structure.

## Features

- **Lexical Analysis**: Tokenizes Mini C source code into meaningful tokens
- **Syntax Analysis**: Builds an AST using recursive descent parsing
- **Error Handling**: Provides detailed error messages with line and column information
- **Pretty Printing**: Displays the AST in a visual tree format
- **Operator Precedence**: Correctly handles arithmetic operator precedence

## Supported Language Features

### Data Types
- `int`: Integer type for variable declarations

### Variable Declarations
```c
int x;
int variable_name;
```

### Assignments
```c
x = 5;
variable_name = expression;
```

### Arithmetic Expressions
- **Operators**: `+`, `-`, `*`, `/`
- **Precedence**: `*` and `/` have higher precedence than `+` and `-`
- **Associativity**: Left-to-right for operators of same precedence
- **Parentheses**: Supported for grouping expressions

### Literals and Identifiers
- **Integer literals**: `0`, `123`, `456`
- **Variable names**: Must start with letter or underscore, followed by letters, digits, or underscores

### Punctuation
- **Semicolon**: `;` - Statement terminator
- **Parentheses**: `(` `)` - Expression grouping

## Grammar Rules

The parser implements the following context-free grammar:

```
Program ::= { Declaration | Assignment }
Declaration ::= 'int' IDENTIFIER ';'
Assignment ::= IDENTIFIER '=' Expression ';'
Expression ::= Term { ('+' | '-') Term }
Term ::= Factor { ('*' | '/') Factor }
Factor ::= NUMBER | IDENTIFIER | '(' Expression ')'
```

## Usage

### Basic Usage

```python
from mini_c_parser import parse_mini_c, ASTPrettyPrinter

# Parse source code
source_code = "int x; x = 5 + 3;"
ast = parse_mini_c(source_code)

# Print the AST
printer = ASTPrettyPrinter()
print(printer.print_ast(ast))
```

### Running the Test Suite

Execute the main script to run all test cases:

```bash
python mini_c_parser.py
```

## Input/Output Examples

### Example 1: Basic Program
**Input:**
```c
int x; int y; x = 5;
```

**Output:**
```
Program
├── VariableDeclaration (type: int, name: x)
├── VariableDeclaration (type: int, name: y)
└── Assignment
    ├── Variable (name: x)
    └── Number (value: 5)
```

### Example 2: Arithmetic Expression
**Input:**
```c
int a; a = 3 + 5;
```

**Output:**
```
Program
├── VariableDeclaration (type: int, name: a)
└── Assignment
    ├── Variable (name: a)
    └── BinaryOperation (operator: +)
        ├── Number (value: 3)
        └── Number (value: 5)
```

### Example 3: Complex Expression with Precedence
**Input:**
```c
int x; int y; x = 5; y = x + 3 * (2 - 1);
```

**Output:**
```
Program
├── VariableDeclaration (type: int, name: x)
├── VariableDeclaration (type: int, name: y)
├── Assignment
│   ├── Variable (name: x)
│   └── Number (value: 5)
└── Assignment
    ├── Variable (name: y)
    └── BinaryOperation (operator: +)
        ├── Variable (name: x)
        └── BinaryOperation (operator: *)
            ├── Number (value: 3)
            └── BinaryOperation (operator: -)
                ├── Number (value: 2)
                └── Number (value: 1)
```

## Error Handling

The parser provides comprehensive error handling with detailed messages:

### Lexical Errors
- **Unexpected characters**: Characters not recognized by the lexer
- **Position information**: Line and column numbers for error location

Example:
```
Lexer Error at 1:10: Unexpected character '@'
```

### Syntax Errors
- **Unexpected tokens**: Tokens that don't match the expected grammar
- **Missing tokens**: Required tokens that are absent
- **Token information**: Details about the problematic token

Example:
```
Parse Error at 1:12: Expected SEMICOLON, got EOF
```

### Error Example
**Input:**
```c
int a; a = 3 + ;
```

**Output:**
```
❌ Parsing failed: Parse Error at 1:12: Unexpected token in expression: SEMICOLON
```

## API Reference

### Classes

#### `Lexer`
Tokenizes source code into a list of tokens.

**Methods:**
- `__init__(source_code: str)`: Initialize with source code
- `tokenize() -> List[Token]`: Return list of tokens

#### `Parser`
Parses tokens into an AST using recursive descent.

**Methods:**
- `__init__(tokens: List[Token])`: Initialize with token list
- `parse() -> Program`: Parse tokens and return AST root

#### `ASTPrettyPrinter`
Formats AST for display.

**Methods:**
- `print_ast(node: ASTNode) -> str`: Return formatted AST string

#### AST Node Classes
- `Program`: Root node containing statements
- `VariableDeclaration`: Variable declaration nodes
- `Assignment`: Assignment statement nodes
- `BinaryOperation`: Binary arithmetic operation nodes
- `Number`: Integer literal nodes
- `Variable`: Variable reference nodes

### Functions

#### `parse_mini_c(source_code: str) -> Program`
Main parsing function that combines lexing and parsing.

**Parameters:**
- `source_code`: String containing Mini C source code

**Returns:**
- `Program`: Root AST node

**Raises:**
- `LexerError`: For lexical analysis errors
- `ParseError`: For syntax parsing errors

## Extending the Parser

### Adding New Token Types

1. Add the token type to the `TokenType` enum:
```python
class TokenType(Enum):
    # ... existing tokens ...
    NEW_TOKEN = "NEW_TOKEN"
```

2. Add the token pattern to the lexer:
```python
self.token_patterns = [
    # ... existing patterns ...
    (r'new_pattern', TokenType.NEW_TOKEN),
]
```

### Adding New AST Node Types

1. Create a new AST node class:
```python
class NewNode(ASTNode):
    def __init__(self, parameter):
        self.parameter = parameter
```

2. Update the pretty printer:
```python
def _print_node(self, node: ASTNode, prefix: str, is_last: bool):
    # ... existing cases ...
    elif isinstance(node, NewNode):
        self.output.append(f"{prefix}{connector}NewNode (parameter: {node.parameter})")
```

### Adding New Grammar Rules

1. Add a new parsing method to the `Parser` class:
```python
def parse_new_construct(self) -> NewNode:
    # Implement parsing logic
    pass
```

2. Update the main parsing loop in `parse()` method to handle the new construct.

### Adding New Operators

1. Add operator tokens to `TokenType` enum
2. Add patterns to lexer
3. Update parsing methods (`parse_expression`, `parse_term`, etc.)
4. Handle precedence and associativity

## Best Practices

1. **Error Recovery**: The parser stops at the first error. For production use, consider implementing error recovery mechanisms.

2. **Symbol Table**: For semantic analysis, implement a symbol table to track variable declarations and scopes.

3. **Type Checking**: Add semantic analysis to verify type compatibility in expressions.

4. **Code Generation**: Extend the AST nodes with methods for code generation or interpretation.

## Limitations

- Only supports integer types
- No support for functions or control structures
- No semantic analysis (type checking, variable scope)
- Limited error recovery
- Single-character operators only

## Troubleshooting

### Common Issues

1. **"Unexpected character" errors**: Check for unsupported characters in source code
2. **"Expected token" errors**: Verify syntax matches the grammar rules
3. **Import errors**: Ensure all required Python modules are available

### Debug Tips

1. Use the lexer separately to examine tokens:
```python
lexer = Lexer(source_code)
tokens = lexer.tokenize()
for token in tokens:
    print(token)
```

2. Add debug prints in parser methods to trace parsing steps

3. Use the pretty printer to visualize partial ASTs during development