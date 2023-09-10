from .vl_agent import ValueLearningAgent
from .ts_agent import TimeSeriesAgent
from .basic_agent import BasicAgent

agent_registry = {
    'value-learning': ValueLearningAgent,
    'time-series': TimeSeriesAgent,
    'basic': BasicAgent,
}
