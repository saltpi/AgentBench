import json

class AgentContext:
    shared: "AgentContext" = None

    @staticmethod
    def create(agent_id, agent_name):
        return AgentContext(agent_id, agent_name)

    def __init__(self, agent_id, agent_name):
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.callstack = []
        self.extra_info = {}
        self.file = open(f"agent_context_{self.agent_id}.jsonl", "a")

    def clear(self):
        self.callstack.clear()
        self.extra_info.clear()
        
    def pretty_print(self):
        print(f"AgentContext for {self.agent_name} (ID: {self.agent_id})")
        print("Callstack:")
        for i, call in enumerate(self.callstack):
            print(f"  Call {i+1}:")
            for key, value in call.items():
                print(f"    {key}: {value}")
        print("Extra Info:")
        for key, value in self.extra_info.items():
            print(f"  {key}: {value}")
    
    def save(self):
        content = json.dump({
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "callstack": self.callstack,
            "extra_info": self.extra_info
        })
        self.file.write(content + "\n")
        self.file.flush()


AgentContext.shared = AgentContext.create("shared", "DefaultAgent")