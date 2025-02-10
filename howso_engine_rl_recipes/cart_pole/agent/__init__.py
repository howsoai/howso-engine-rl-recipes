from .ts_agent import TimeSeriesAgent
from .basic_agent import BasicAgent

agent_registry = {
    'time-series': TimeSeriesAgent,
    'basic': BasicAgent,
}
