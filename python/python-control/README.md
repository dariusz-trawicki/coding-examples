# Example: PID controller for a second-order plant – step response simulation

## Running the example with uv

```bash
uv venv
uv sync

uv run python pid_simulation.py
```

This will display two plots:
- y(t) – system output (closed-loop step response),
- u(t) – control signal.

The script pauses while the plots are open.
After closing the figures, it continues and prints:

```text
Plant G(s) = ...
Controller C(s) = ...
Closed-loop T(s) = ...
```