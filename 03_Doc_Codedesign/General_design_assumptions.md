# Design decision:
Use pandas for IO + cleaning, convert to numpy/numba or similar only for performance-critical loops
- io_smash.py serves as file reader on a more general basis to also cover simpler particle list outputs, which can be used e.g. to test calculation functions
- 
