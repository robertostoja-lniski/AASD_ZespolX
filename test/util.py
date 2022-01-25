from spade.agent import Agent


def get_messages_to(agent: Agent):
    return [msg[1] for msg in agent.traces.all() if msg[1].to == agent.jid]


def get_messages_to_from(agent_to: Agent, agent_from: Agent):
    return [msg[1] for msg in agent_to.traces.all() if msg[1].to == agent_to.jid and msg[1].sender == agent_from.jid]
