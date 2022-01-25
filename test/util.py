from spade.agent import Agent


def get_messages_to(agent: Agent):
    return [msg[1] for msg in agent.traces.all() if msg[1].to == agent.jid]
