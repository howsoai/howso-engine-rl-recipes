import logging
import pytest
from multiprocessing import cpu_count

from howso_engine_rl_recipes.simulation import GameType, Simulation

logger = logging.getLogger("howso.rl.tests")


@pytest.mark.regression
@pytest.mark.parametrize('agent_type, iterations, max_avg_rounds', [
    ('basic', 14, 1000),
])
def test_agents_regression(agent_type, iterations, max_avg_rounds):
    """Test cart pole is solved by all agent types."""
    max_workers = int(cpu_count() / 2 - 1)
    sim = Simulation(iterations=iterations, max_workers=max_workers)
    results = sim.run(game_type=GameType.CART_POLE, agent_type=agent_type,
                      max_rounds=max_avg_rounds)

    logger.info({
        "agent_type": agent_type,
        "iterations": iterations,
        "max_avg_rounds": max_avg_rounds,
        "results": results
    })

    assert len(results['runs']) == iterations

    metrics = results['metrics']
    assert metrics['percent-won'] >= 50
    assert metrics['average-rounds-to-win'] < max_avg_rounds
    assert metrics['average-win-high-score'] >= 300


@pytest.mark.experimental
@pytest.mark.parametrize('agent_type, iterations, max_avg_rounds', [
    ('time-series', 8, 1000),
])
def test_agents_experimental(agent_type, iterations, max_avg_rounds):
    """Test cart pole is solved by all agent types."""
    max_workers = int(cpu_count() / 2 - 1)
    sim = Simulation(iterations=iterations, max_workers=max_workers)
    results = sim.run(game_type=GameType.CART_POLE, agent_type=agent_type,
                      max_rounds=1000)

    logger.info({
        "agent_type": agent_type,
        "iterations": iterations,
        "max_avg_rounds": max_avg_rounds,
        "results": results
    })

    assert len(results['runs']) == iterations

    metrics = results['metrics']
    assert metrics['total-won'] >= 4
    assert metrics['average-rounds-to-win'] < max_avg_rounds
    assert metrics['average-win-high-score'] >= 300
