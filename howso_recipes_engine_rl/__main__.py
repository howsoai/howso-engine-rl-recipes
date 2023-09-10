import sys

from .simulation import Simulation


if __name__ == '__main__':
    # CLI entrypoint when run via `python -m howso_recipes_engine_rl`
    Simulation.entrypoint(sys.argv[1:])
