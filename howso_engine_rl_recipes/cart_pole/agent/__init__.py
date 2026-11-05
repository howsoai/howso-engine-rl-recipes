from .ts_agent import TimeSeriesAgent
from .basic_agent import BasicAgent
from .stability_agent import StabilityAgent

agent_registry = {
    'time-series': TimeSeriesAgent,
    'basic': BasicAgent,
    'stability': StabilityAgent,
}
