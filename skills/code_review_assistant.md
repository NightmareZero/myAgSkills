# Code Review Assistant

## Description
Analyzes code changes and provides constructive feedback on code quality, best practices, potential bugs, and improvement suggestions.

## Category
Development

## Input Parameters
- `code`: The code to review (string or file path)
- `language`: Programming language (e.g., "python", "javascript", "java")
- `focus_areas`: Specific areas to focus on (optional, array: ["security", "performance", "readability", "best_practices"])

## Output
A structured code review with:
- Overall assessment
- Specific issues found with line numbers
- Suggestions for improvement
- Security concerns (if any)

## Usage Example
```
Input:
  code: "def calculate(x, y):\n    return x/y"
  language: "python"
  focus_areas: ["security", "best_practices"]

Output:
  Issues Found:
  - Line 2: Potential ZeroDivisionError - add validation for y != 0
  - Missing docstring for function
  - Consider adding type hints
  
  Suggestions:
  - Add error handling for division by zero
  - Add descriptive docstring explaining parameters
  - Use type hints: def calculate(x: float, y: float) -> float
```

## Dependencies
- Static code analysis tools
- Language-specific linters
- Security scanning capabilities

## Notes
- Supports major programming languages
- Can be customized for specific coding standards
- Best used as part of code review workflow
