# Armstrong Numbers Calculator

This is a web application built with Django that calculates Armstrong numbers within a given range. An Armstrong number is a number that is equal to the sum of its own digits each raised to the power of the number of digits.

## Features

*   Calculates Armstrong numbers in a specified range.
*   Provides a simple and easy-to-use web interface.
*   Includes a REST API for programmatic access.
*   Handles user input validation and provides clear error messages.

### REST API

The API endpoint `/api/armstrong-numbers/` allows you to find Armstrong numbers programmatically.

Send `start_range`, `end_range` and optionally `engine` (`"python"` or `"c"`, default `"python"`). The response includes the numbers found, the engine used and `elapsed_ms`.

### Engines

Both engines use the same algorithm: instead of checking every number in the range, they try each combination of digits once (153, 135, 315... all share the digits {1, 3, 5}), so large ranges finish quickly.

*   **Python** (`armstrong_nums/armstrong.py`) — end range up to 10^15.
*   **C** (`armstrong_nums/c_ext/armstrong.c`) — about 20x faster, end range up to 2^64 - 1. Python loads it with `ctypes` and compiles it automatically on first use, so a C compiler (`cc` or `gcc`) must be available. To build it ahead of time, e.g. in your deploy build command:

```bash
python -c "from armstrong_nums import c_engine; c_engine.build()"
```
