import sys

from .simulation import Simulation


if __name__ == '__main__':
    # CLI entrypoint when run via `python -m howso_engine_rl_recipes`
    Simulation.entrypoint(sys.argv[1:])
