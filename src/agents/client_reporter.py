from src.agents.base_agent import BaseAgent


class ClientReporter(BaseAgent):
    class Behaviour(BaseAgent.BaseAgentBehaviour):
        async def run(self):
            await super().run()
            pass

    def __init__(self, username: str, password: str, host: str):
        super().__init__(username, password, host)
        self.behaviour = self.Behaviour()

    async def setup(self):
        self.add_behaviour(self.behaviour)
        await super().setup()

