#!/usr/bin/env python3
"""
Tests for Mini C Parser
Simple tests to verify the parser works correctly.
"""

from mini_c_parser import parse_mini_c, ASTPrettyPrinter, LexerError, ParseError


def test_simple_variable():
    """Test: int x;"""
    print("Test: Simple variable declaration")
    code = "int x;"
    
    try:
        ast = parse_mini_c(code)
        printer = ASTPrettyPrinter()
        print(f"Code: {code}")
        print("Result:")
        print(printer.print_ast(ast))
        print("✓ PASSED\n")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        return False


def test_simple_assignment():
    """Test: int x; x = 5;"""
    print("Test: Simple assignment")
    code = "int x; x = 5;"
    
    try:
        ast = parse_mini_c(code)
        printer = ASTPrettyPrinter()
        print(f"Code: {code}")
        print("Result:")
        print(printer.print_ast(ast))
        print("✓ PASSED\n")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        return False


def test_addition():
    """Test: int x; x = 3 + 5;"""
    print("Test: Addition")
    code = "int x; x = 3 + 5;"
    
    try:
        ast = parse_mini_c(code)
        printer = ASTPrettyPrinter()
        print(f"Code: {code}")
        print("Result:")
        print(printer.print_ast(ast))
        print("✓ PASSED\n")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        return False


def test_multiplication():
    """Test: int x; x = 3 * 4;"""
    print("Test: Multiplication")
    code = "int x; x = 3 * 4;"
    
    try:
        ast = parse_mini_c(code)
        printer = ASTPrettyPrinter()
        print(f"Code: {code}")
        print("Result:")
        print(printer.print_ast(ast))
        print("✓ PASSED\n")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        return False


def test_precedence():
    """Test: int x; x = 2 + 3 * 4; (should be 2 + (3 * 4))"""
    print("Test: Operator precedence (* before +)")
    code = "int x; x = 2 + 3 * 4;"
    
    try:
        ast = parse_mini_c(code)
        printer = ASTPrettyPrinter()
        print(f"Code: {code}")
        print("Result (should show 3*4 calculated first):")
        print(printer.print_ast(ast))
        print("✓ PASSED\n")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        return False


def test_parentheses():
    """Test: int x; x = (2 + 3) * 4; (should be (2 + 3) * 4)"""
    print("Test: Parentheses grouping")
    code = "int x; x = (2 + 3) * 4;"
    
    try:
        ast = parse_mini_c(code)
        printer = ASTPrettyPrinter()
        print(f"Code: {code}")
        print("Result (should show 2+3 calculated first):")
        print(printer.print_ast(ast))
        print("✓ PASSED\n")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        return False


def test_variables_in_expression():
    """Test: int x; int y; x = 5; y = x + 3;"""
    print("Test: Using variables in expressions")
    code = "int x; int y; x = 5; y = x + 3;"
    
    try:
        ast = parse_mini_c(code)
        printer = ASTPrettyPrinter()
        print(f"Code: {code}")
        print("Result:")
        print(printer.print_ast(ast))
        print("✓ PASSED\n")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        return False


def test_syntax_error():
    """Test: int x; x = 5 +; (should fail - missing operand)"""
    print("Test: Syntax error detection")
    code = "int x; x = 5 +;"
    
    try:
        ast = parse_mini_c(code)
        print(f"Code: {code}")
        print("✗ FAILED: Should have detected syntax error\n")
        return False
    except (LexerError, ParseError) as e:
        print(f"Code: {code}")
        print(f"Correctly caught error: {e}")
        print("✓ PASSED\n")
        return True
    except Exception as e:
        print(f"✗ FAILED: Wrong error type: {e}\n")
        return False


def test_invalid_character():
    """Test: int x; x = 5 @ 3; (should fail - @ is invalid)"""
    print("Test: Invalid character detection")
    code = "int x; x = 5 @ 3;"
    
    try:
        ast = parse_mini_c(code)
        print(f"Code: {code}")
        print("✗ FAILED: Should have detected invalid character\n")
        return False
    except LexerError as e:
        print(f"Code: {code}")
        print(f"Correctly caught error: {e}")
        print("✓ PASSED\n")
        return True
    except Exception as e:
        print(f"✗ FAILED: Wrong error type: {e}\n")
        return False


def run_all_tests():
    """Run all tests and show results"""
    print("=" * 50)
    print("MINI C PARSER TESTS")
    print("=" * 50)
    print()
    
    # All test functions
    tests = [
        test_simple_variable,
        test_simple_assignment,
        test_addition,
        test_multiplication,
        test_precedence,
        test_parentheses,
        test_variables_in_expression,
        test_syntax_error,
        test_invalid_character
    ]
    
    # Run tests
    results = []
    for test in tests:
        result = test()
        results.append(result)
    
    # Show summary
    print("=" * 50)
    print("SUMMARY")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    for i, (test, result) in enumerate(zip(tests, results), 1):
        status = "PASS" if result else "FAIL"
        print(f"{i}. {test.__doc__} - {status}")
    
    print(f"\nResult: {passed}/{total} tests passed")
    
    if passed == total:
        print("SUCCESS: All tests passed!")
    else:
        print(f"FAILURE: {total - passed} test(s) failed")
    
    return passed == total


if __name__ == "__main__":
    run_all_tests() 