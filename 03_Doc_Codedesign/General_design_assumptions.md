# General script design (best practice)
## General guideline
Content-related stuff goes together, but:
- Definitions before their usage
- abstract → concrete
- Low-level → High-level
## Ordering
Best practice for ordering structure in a Python script:
- Shebang & Encoding (optional)
- Imports: first standard libs, then third-party libs, then own modules (separated by empty lines)
- Constants and configurations
- Helper functions (low-level like parser, small mathematical helpers, string manipulators, I/O helper) should always come before classes
- Classes (only one main class per script to follow "single responsibility" approach)
- High-level functions / pipelines (workflow functions, glue code, combinations of multiple classes/functions)
- if `__name__ == "__main__":` entry point (scripts can be imported or run individually e.g. for testing)

# Design decision:
Use pandas for IO + cleaning, convert to numpy/numba or similar only for performance-critical loops
- io_smash.py serves as file reader on a more general basis to also cover simpler particle list outputs, which can be used e.g. to test calculation functions
- 
