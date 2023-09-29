import logging
import pytest

from howso_recipes_engine_rl.simulation import GameType, Simulation

logger = logging.getLogger("howso.rl.tests")


@pytest.mark.regression
@pytest.mark.parametrize('agent_type, iterations, max_avg_rounds', [
    ('basic', 3, 500),
    ('value-learning', 3, 500),
])
def test_agents_regression(agent_type, iterations, max_avg_rounds):
    """Test cart pole is solved by all agent types."""
    sim = Simulation(iterations=iterations, max_workers=iterations)
    results = sim.run(game_type=GameType.CART_POLE, agent_type=agent_type,
                      max_rounds=600)

    logger.info({
        "agent_type": agent_type,
        "iterations": iterations,
        "max_avg_rounds": max_avg_rounds,
        "results": results
    })

    assert len(results['runs']) == iterations

    metrics = results['metrics']
    assert metrics['percent-won'] >= 25
    assert metrics['average-rounds-to-win'] < max_avg_rounds
    assert metrics['average-win-high-score'] >= 300


@pytest.mark.experimental
@pytest.mark.parametrize('agent_type, iterations, max_avg_rounds', [
    ('time-series', 5, 1000),
])
def test_agents_experimental(agent_type, iterations, max_avg_rounds):
    """Test cart pole is solved by all agent types."""
    sim = Simulation(iterations=iterations, max_workers=iterations)
    results = sim.run(game_type=GameType.CART_POLE, agent_type=agent_type,
                      max_rounds=1_200)

    logger.info({
        "agent_type": agent_type,
        "iterations": iterations,
        "max_avg_rounds": max_avg_rounds,
        "results": results
    })

    assert len(results['runs']) == iterations

    metrics = results['metrics']
    assert metrics['total-won'] >= 2
    assert metrics['average-rounds-to-win'] < max_avg_rounds
    assert metrics['average-win-high-score'] >= 300
