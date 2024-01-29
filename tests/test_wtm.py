import logging
import pytest
from multiprocessing import cpu_count

from howso_engine_rl_recipes.simulation import GameType, Simulation

logger = logging.getLogger("howso.rl.tests")


@pytest.mark.regression
@pytest.mark.parametrize('agent_type, iterations', [
    ('basic', 30),
])
def test_wafer_thin_mint(agent_type, iterations):
    max_workers = int(cpu_count() / 2 - 1)
    sim = Simulation(iterations=iterations, max_workers=max_workers)
    results = sim.run(game_type=GameType.WTM, agent_type=agent_type)
    logger.info({
        "agent_type": agent_type,
        "iterations": iterations,
        "results": results
    })

    assert len(results['runs']) == iterations

    metrics = results['metrics']
    assert metrics['percent-won'] >= 70
    assert metrics['average-win-high-score'] == 9
    assert metrics['average-rounds-to-win'] > 2

    # Make sure there are at least 2 cases or games, which is the minimum to
    # learn the domain.
    for run in results['runs'].values():
        if run['win']:
            assert run['total_cases'] >= 2
