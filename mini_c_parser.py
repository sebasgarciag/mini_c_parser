#!/usr/bin/env python3
"""
Mini C Programming Language Parser
A complete syntax analyzer that reads tokens and generates an Abstract Syntax Tree (AST).

This is like building a translator that understands a simple programming language.
Think of it as teaching the computer to read and understand Mini C code step by step.
"""

# We need these imports to make our parser work
import re                    # For pattern matching (finding tokens in text)
from enum import Enum        # For creating named constants (token types)
from typing import List, Optional, Union  # For type hints (makes code clearer)
from dataclasses import dataclass         # For simple data containers


class TokenType(Enum):
    """
    These are all the different types of "words" our Mini C language understands.
    Think of this like a vocabulary list - each type represents a different kind of word.
    """
    # Keywords (special reserved words)
    INT = "INT"              # The word "int" for declaring variables
    
    # Identifiers and literals (names and values)
    IDENTIFIER = "IDENTIFIER"  # Variable names like "x", "myVar", "counter"
    NUMBER = "NUMBER"         # Numbers like 5, 123, 0
    
    # Operators (symbols that do math)
    PLUS = "PLUS"            # The + symbol
    MINUS = "MINUS"          # The - symbol  
    MULTIPLY = "MULTIPLY"    # The * symbol
    DIVIDE = "DIVIDE"        # The / symbol
    ASSIGN = "ASSIGN"        # The = symbol (for assignments)
    
    # Punctuation (symbols that organize code)
    SEMICOLON = "SEMICOLON"  # The ; symbol (ends statements)
    LPAREN = "LPAREN"        # The ( symbol (left parenthesis)
    RPAREN = "RPAREN"        # The ) symbol (right parenthesis)
    
    # Special markers
    EOF = "EOF"              # End of file - tells us we're done reading


@dataclass
class Token:
    """
    A Token is like a single word or symbol that we found in the code.
    It remembers what type it is, what it says, and where we found it.
    
    For example: if we see "int" in the code, we create a Token that says:
    - type: INT (it's a keyword)
    - value: "int" (the actual text)
    - line: 1, column: 5 (where we found it)
    """
    type: TokenType    # What kind of token this is (INT, NUMBER, PLUS, etc.)
    value: str         # The actual text we found ("int", "5", "+", etc.)
    line: int          # Which line of code this was on (starts at 1)
    column: int        # Which column on that line (starts at 1)
    
    def __str__(self):
        """Make it easy to print tokens for debugging"""
        return f"Token({self.type.value}, '{self.value}', {self.line}:{self.column})"


class LexerError(Exception):
    """
    This error happens when we find something in the code that we don't understand.
    Like finding a @ symbol when we only know letters, numbers, and basic symbols.
    """
    def __init__(self, message: str, line: int, column: int):
        self.message = message  # What went wrong
        self.line = line       # Where it happened (line number)
        self.column = column   # Where it happened (column number)
        # Create a helpful error message that shows exactly where the problem is
        super().__init__(f"Lexer Error at {line}:{column}: {message}")


class ParseError(Exception):
    """
    This error happens when the tokens are in the wrong order.
    Like writing "int = x;" instead of "int x;" - the words are fine but the order is wrong.
    """
    def __init__(self, message: str, token: Token):
        self.message = message  # What went wrong
        self.token = token     # The token that caused the problem
        # Create a helpful error message using the token's position
        super().__init__(f"Parse Error at {token.line}:{token.column}: {message}")


class Lexer:
    """
    The Lexer is like a scanner that reads through code character by character
    and groups them into meaningful tokens (words and symbols).
    
    Think of it like reading a sentence and identifying each word and punctuation mark.
    """
    
    def __init__(self, source_code: str):
        # Store the code we want to analyze
        self.source = source_code
        
        # Keep track of where we are in the code
        self.position = 0    # Which character we're looking at (starts at 0)
        self.line = 1        # Which line we're on (starts at 1)
        self.column = 1      # Which column we're on (starts at 1)
        
        # This will store all the tokens we find
        self.tokens = []
        
        # These are the patterns we look for to identify different types of tokens
        # Each pattern is a regular expression that matches specific text
        self.token_patterns = [
            (r'\bint\b', TokenType.INT),                    # The word "int" (whole word only)
            (r'[a-zA-Z_][a-zA-Z0-9_]*', TokenType.IDENTIFIER),  # Variable names (start with letter/underscore)
            (r'\d+', TokenType.NUMBER),                     # Numbers (one or more digits)
            (r'\+', TokenType.PLUS),                        # Plus sign
            (r'-', TokenType.MINUS),                        # Minus sign
            (r'\*', TokenType.MULTIPLY),                    # Multiply sign (escaped because * is special in regex)
            (r'/', TokenType.DIVIDE),                       # Divide sign
            (r'=', TokenType.ASSIGN),                       # Assignment sign
            (r';', TokenType.SEMICOLON),                    # Semicolon
            (r'\(', TokenType.LPAREN),                      # Left parenthesis (escaped)
            (r'\)', TokenType.RPAREN),                      # Right parenthesis (escaped)
        ]
        
        # Pre-compile the patterns for faster matching (optimization)
        self.compiled_patterns = [(re.compile(pattern), token_type) 
                                for pattern, token_type in self.token_patterns]
    
    def current_char(self) -> Optional[str]:
        """
        Look at the character we're currently pointing to.
        Returns None if we've reached the end of the code.
        """
        if self.position >= len(self.source):
            return None  # We've read all the code
        return self.source[self.position]
    
    def advance(self):
        """
        Move our pointer to the next character.
        Also keeps track of which line and column we're on.
        """
        if self.position < len(self.source):
            # If we just read a newline, move to the next line
            if self.source[self.position] == '\n':
                self.line += 1
                self.column = 1  # Reset to start of new line
            else:
                self.column += 1  # Move to next column on same line
            self.position += 1    # Move to next character
    
    def skip_whitespace(self):
        """
        Skip over spaces, tabs, newlines, etc.
        We don't care about whitespace for tokens, but we need to track position.
        """
        while self.current_char() and self.current_char().isspace():
            self.advance()
    
    def tokenize(self) -> List[Token]:
        """
        This is the main method that breaks down the entire source code into tokens.
        It's like reading through a sentence and identifying each word and punctuation.
        """
        self.tokens = []  # Start with an empty list of tokens
        
        # Keep reading until we've gone through all the code
        while self.position < len(self.source):
            # Skip any spaces, tabs, newlines, etc.
            self.skip_whitespace()
            
            # If we've reached the end after skipping whitespace, we're done
            if self.position >= len(self.source):
                break
            
            # Try to match the current position against each of our token patterns
            matched = False
            for pattern, token_type in self.compiled_patterns:
                # See if this pattern matches at our current position
                match = pattern.match(self.source, self.position)
                if match:
                    # We found a match! Get the text that matched
                    value = match.group(0)
                    
                    # Create a token with the type, value, and current position
                    token = Token(token_type, value, self.line, self.column)
                    self.tokens.append(token)
                    
                    # Move our position forward by the length of what we just matched
                    for _ in range(len(value)):
                        self.advance()
                    
                    matched = True
                    break  # Stop trying other patterns since we found a match
            
            # If we couldn't match anything, that's an error
            if not matched:
                char = self.current_char()
                raise LexerError(f"Unexpected character '{char}'", self.line, self.column)
        
        # Add a special EOF (End Of File) token to mark the end
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens


# AST Node Classes
# These classes represent different parts of our program as a tree structure
# Think of it like a family tree, but for code!

class ASTNode:
    """
    This is the base class for all parts of our syntax tree.
    Every piece of code (variables, numbers, operations) will be a type of ASTNode.
    """
    pass


class Program(ASTNode):
    """
    This represents the entire program - it's the root of our tree.
    It contains a list of all the statements in the program.
    Like: int x; int y; x = 5; (three statements)
    """
    def __init__(self, statements: List[ASTNode]):
        self.statements = statements  # List of all statements in the program


class VariableDeclaration(ASTNode):
    """
    This represents declaring a variable, like "int x;"
    It remembers the type (int) and the name (x).
    """
    def __init__(self, var_type: str, name: str):
        self.var_type = var_type  # The type of variable ("int")
        self.name = name         # The name of the variable ("x")


class Assignment(ASTNode):
    """
    This represents assigning a value to a variable, like "x = 5;"
    It has two parts: the variable being assigned to, and the value being assigned.
    """
    def __init__(self, variable: 'Variable', expression: ASTNode):
        self.variable = variable      # The variable we're assigning to (left side)
        self.expression = expression  # The value we're assigning (right side)


class BinaryOperation(ASTNode):
    """
    This represents operations with two parts, like "5 + 3" or "x * 2"
    It has a left side, an operator, and a right side.
    """
    def __init__(self, left: ASTNode, operator: str, right: ASTNode):
        self.left = left          # Left side of the operation
        self.operator = operator  # The operator (+, -, *, /)
        self.right = right        # Right side of the operation


class Number(ASTNode):
    """
    This represents a number in the code, like 5, 123, or 0.
    """
    def __init__(self, value: int):
        self.value = value  # The actual number value


class Variable(ASTNode):
    """
    This represents using a variable name in the code, like "x" or "myVar".
    """
    def __init__(self, name: str):
        self.name = name  # The name of the variable


class Parser:
    """
    The Parser takes the tokens from the Lexer and builds them into a syntax tree.
    It's like taking a pile of words and arranging them into a proper sentence structure.
    
    This uses "recursive descent" - it breaks down complex things into simpler parts,
    then breaks those parts down further, like solving a puzzle piece by piece.
    """
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens  # All the tokens we got from the lexer
        self.position = 0     # Which token we're currently looking at
        # Start by looking at the first token (if there are any)
        self.current_token = self.tokens[0] if tokens else None
    
    def advance(self):
        """
        Move to the next token in our list.
        Like turning the page to read the next word.
        """
        if self.position < len(self.tokens) - 1:
            self.position += 1
            self.current_token = self.tokens[self.position]
    
    def expect(self, token_type: TokenType) -> Token:
        """
        This says "I expect to see a specific type of token here."
        If we don't see what we expect, that's a syntax error.
        
        For example, after "int" we expect to see an identifier (variable name).
        """
        if self.current_token.type != token_type:
            raise ParseError(f"Expected {token_type.value}, got {self.current_token.type.value}", 
                           self.current_token)
        token = self.current_token  # Save the token we found
        self.advance()              # Move to the next token
        return token               # Return the token we just consumed
    
    def parse(self) -> Program:
        """
        This is the main parsing method - it reads the entire program.
        It keeps reading statements until it reaches the end of the file.
        """
        statements = []  # We'll collect all the statements here
        
        # Keep reading statements until we hit the end of file
        while self.current_token.type != TokenType.EOF:
            # Look at the current token to decide what kind of statement this is
            if self.current_token.type == TokenType.INT:
                # If it starts with "int", it's a variable declaration
                statements.append(self.parse_declaration())
            elif self.current_token.type == TokenType.IDENTIFIER:
                # If it starts with a variable name, it's an assignment
                statements.append(self.parse_assignment())
            else:
                # If it's something else, we don't know what to do with it
                raise ParseError(f"Unexpected token {self.current_token.type.value}", 
                               self.current_token)
        
        # Create and return a Program node containing all our statements
        return Program(statements)
    
    def parse_declaration(self) -> VariableDeclaration:
        """
        Parse a variable declaration like "int x;"
        
        The pattern is: 'int' IDENTIFIER ';'
        Example: int myVariable;
        """
        self.expect(TokenType.INT)        # Must start with "int"
        name_token = self.expect(TokenType.IDENTIFIER)  # Then a variable name
        self.expect(TokenType.SEMICOLON)  # Then a semicolon
        
        # Create a VariableDeclaration node with the type and name
        return VariableDeclaration("int", name_token.value)
    
    def parse_assignment(self) -> Assignment:
        """
        Parse an assignment like "x = 5;" or "y = x + 3;"
        
        The pattern is: IDENTIFIER '=' Expression ';'
        Example: myVariable = 42;
        """
        name_token = self.expect(TokenType.IDENTIFIER)  # Variable name
        self.expect(TokenType.ASSIGN)     # The = sign
        expression = self.parse_expression()  # The value being assigned (could be complex)
        self.expect(TokenType.SEMICOLON)  # Semicolon to end the statement
        
        # Create Variable and Assignment nodes
        variable = Variable(name_token.value)
        return Assignment(variable, expression)
    
    def parse_expression(self) -> ASTNode:
        """
        Parse an expression with + and - operators.
        
        This handles the lowest precedence operators (+ and -).
        The pattern is: Term { ('+' | '-') Term }
        Example: 5 + 3 - 2 becomes ((5 + 3) - 2)
        """
        left = self.parse_term()  # Start with a term (higher precedence)
        
        # Keep looking for + or - operators
        while self.current_token.type in [TokenType.PLUS, TokenType.MINUS]:
            operator = self.current_token.value  # Save the operator (+ or -)
            self.advance()                       # Move past the operator
            right = self.parse_term()           # Get the next term
            # Create a binary operation and make it the new left side
            # This makes operations left-associative: 5 + 3 + 2 = (5 + 3) + 2
            left = BinaryOperation(left, operator, right)
        
        return left
    
    def parse_term(self) -> ASTNode:
        """
        Parse a term with * and / operators.
        
        This handles higher precedence operators (* and /).
        The pattern is: Factor { ('*' | '/') Factor }
        Example: 5 * 3 / 2 becomes ((5 * 3) / 2)
        """
        left = self.parse_factor()  # Start with a factor (highest precedence)
        
        # Keep looking for * or / operators
        while self.current_token.type in [TokenType.MULTIPLY, TokenType.DIVIDE]:
            operator = self.current_token.value  # Save the operator (* or /)
            self.advance()                       # Move past the operator
            right = self.parse_factor()         # Get the next factor
            # Create a binary operation and make it the new left side
            left = BinaryOperation(left, operator, right)
        
        return left
    
    def parse_factor(self) -> ASTNode:
        """
        Parse a factor - the basic building blocks of expressions.
        
        A factor can be:
        - A number (like 42)
        - A variable (like x)
        - A parenthesized expression (like (5 + 3))
        """
        if self.current_token.type == TokenType.NUMBER:
            # It's a number - convert to integer and create a Number node
            value = int(self.current_token.value)
            self.advance()
            return Number(value)
        
        elif self.current_token.type == TokenType.IDENTIFIER:
            # It's a variable name - create a Variable node
            name = self.current_token.value
            self.advance()
            return Variable(name)
        
        elif self.current_token.type == TokenType.LPAREN:
            # It's a parenthesized expression - parse what's inside
            self.advance()  # Skip the opening (
            expression = self.parse_expression()  # Parse the expression inside
            self.expect(TokenType.RPAREN)        # Make sure there's a closing )
            return expression  # Return the expression (parentheses are just for grouping)
        
        else:
            # We don't recognize this token in an expression
            raise ParseError(f"Unexpected token in expression: {self.current_token.type.value}", 
                           self.current_token)


class ASTPrettyPrinter:
    """
    This class makes our syntax tree look nice when we print it.
    It creates a visual tree structure with lines and branches,
    like a family tree or file explorer.
    """
    
    def __init__(self):
        self.output = []  # We'll build up the output lines here
    
    def print_ast(self, node: ASTNode, prefix: str = "", is_last: bool = True) -> str:
        """
        This is the main method to print an AST node as a pretty tree.
        It returns a string that shows the tree structure visually.
        """
        self.output = []  # Start with empty output
        self._print_node(node, "", True)  # Start printing from the root
        return "\n".join(self.output)    # Join all lines with newlines
    
    def _print_node(self, node: ASTNode, prefix: str, is_last: bool):
        """
        This method recursively prints each node in the tree.
        It figures out what type of node it is and prints it appropriately.
        """
        # Choose the right connector symbol based on whether this is the last child
        connector = "└── " if is_last else "├── "
        
        if isinstance(node, Program):
            # The Program node is the root - it contains all statements
            self.output.append(f"{prefix}Program")
            for i, statement in enumerate(node.statements):
                is_last_child = i == len(node.statements) - 1  # Is this the last statement?
                # Create the prefix for child nodes (adds spacing or vertical line)
                child_prefix = prefix + ("    " if is_last else "│   ")
                self._print_node(statement, child_prefix, is_last_child)
        
        elif isinstance(node, VariableDeclaration):
            # Variable declarations are simple - just show the type and name
            self.output.append(f"{prefix}{connector}VariableDeclaration (type: {node.var_type}, name: {node.name})")
        
        elif isinstance(node, Assignment):
            # Assignments have two parts: the variable and the expression
            self.output.append(f"{prefix}{connector}Assignment")
            child_prefix = prefix + ("    " if is_last else "│   ")
            self._print_node(node.variable, child_prefix, False)    # Variable is not last
            self._print_node(node.expression, child_prefix, True)   # Expression is last
        
        elif isinstance(node, BinaryOperation):
            # Binary operations have two parts: left and right, with an operator
            self.output.append(f"{prefix}{connector}BinaryOperation (operator: {node.operator})")
            child_prefix = prefix + ("    " if is_last else "│   ")
            self._print_node(node.left, child_prefix, False)   # Left side is not last
            self._print_node(node.right, child_prefix, True)   # Right side is last
        
        elif isinstance(node, Number):
            # Numbers are simple - just show the value
            self.output.append(f"{prefix}{connector}Number (value: {node.value})")
        
        elif isinstance(node, Variable):
            # Variables are simple - just show the name
            self.output.append(f"{prefix}{connector}Variable (name: {node.name})")


def parse_mini_c(source_code: str) -> Program:
    """
    This is the main function that takes Mini C source code and returns an AST.
    It's like a one-stop shop - give it code, get back a syntax tree.
    
    This function combines the lexer and parser to do the complete analysis.
    """
    try:
        # Step 1: Break the source code into tokens (lexical analysis)
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        
        # Step 2: Build the syntax tree from tokens (syntax analysis)
        parser = Parser(tokens)
        ast = parser.parse()
        
        return ast
    
    except (LexerError, ParseError) as e:
        # If anything goes wrong, print the error and re-raise it
        print(f"Error: {e}")
        raise


def demo():
    """
    Simple demonstration of the Mini C parser.
    For comprehensive tests, run: python test_mini_c_parser.py
    """
    print("Mini C Parser Demo")
    print("=" * 40)
    
    # Simple demo code
    code = "int x; int y; x = 5; y = x + 3 * 2;"
    
    print(f"Parsing: {code}")
    print("-" * 40)
    
    try:
        # Parse the code
        ast = parse_mini_c(code)
        
        # Display the result
        printer = ASTPrettyPrinter()
        print("AST:")
        print(printer.print_ast(ast))
        print("\n[SUCCESS] Demo completed successfully!")
        print("\nFor comprehensive tests, run: python test_mini_c_parser.py")
        
    except Exception as e:
        print(f"[ERROR] Demo failed: {e}")


# This is the standard Python way to run the demo when the script is executed
if __name__ == "__main__":
    demo() 