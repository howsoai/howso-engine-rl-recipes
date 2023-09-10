# Howso Engine&trade; RL Recipes

This package contains a set of examples of using [Howso Engine](https://github.com/howsoai/howso-engine) for
Reinforcement Learning projects.

## Installation

### Interactively modified source "installation"

Howso encourages users to unzip the archive into a local directory and
interactively run and modify the code to explore the various ways that
Howso Engine can be leveraged in Reinforcement Learning scenarios.

To do this, simply expand the ZIP file into a directory of your choice, create
a Python virtual environment, install the requirements appropriate for your
version of Python.

At this point, you can navigate into the root of the expanded package,
"howso-recipes-engine-rl". Now, you can run the various examples from here
as "modules". See the instructions below for the example you'd like to run.

Each of the examples offers interactive help for the supported parameters. This
is invoked with:

    python -m howso_recipes_engine_rl --help


### Installation as a Python package

Sometimes it can be beneficial to install this package into an existing
Python environment for running. In this case use:

`pip install howso-recipes-engine-rl`

Or, if installing from a file-based distribution use:

`pip install -e [path/to/uncompressed/distribution]/howso-recipes-engine-rl/`


## Available Reinforcement Learning Examples

### Wafer Thin Mint

An implementation of the wafer_thin_mint game where a player attempts to
eat wafer-thin mints and avoid exploding.

Based on the paper:
Bontrager, Philip, Ahmed Khalifa, Damien Anderson, Matthew Stephenson,
Christoph Salge, and Julian Togelius. '"Superstition" in the Network: Deep
Reinforcement Learning Plays Deceptive Games.' In Proceedings of the
AAAI Conference on Artificial Intelligence and Interactive Digital
Entertainment, vol. 15, no. 1, pp. 10-16. 2019.
https://www.aaai.org/ojs/index.php/AIIDE/article/download/5218/5074


To run this example with the default options use:

    python -m howso_recipes_engine_rl wtm

To see all the available options use:

    python -m howso_recipes_engine_rl wtm --help

### Cart Pole

This example leverages the Farama-Foundation Gymnasium (Formerly OpenAI Gym)
"playground" for RL projects.

See: https://gymnasium.farama.org/environments/classic_control/cart_pole/

From the project description:
This environment corresponds to the version of the cart-pole problem described
by Barto, Sutton, and Anderson in “[Neuronlike Adaptive Elements That Can Solve
Difficult Learning Control Problem](https://ieeexplore.ieee.org/document/6313077)”.
A pole is attached by an un-actuated joint
to a cart, which moves along a frictionless track. The pendulum is placed
upright on the cart and the goal is to balance the pole by applying forces in
the left and right direction on the cart.


To run this example with the default options use:

    python -m howso_recipes_engine_rl cartpole

To see all the available options including different agent types that have
been implemented use:

    python -m howso_recipes_engine_rl cartpole --help

## License

[License](LICENSE.txt)

## Contributing

[Contributing](CONTRIBUTING.md)