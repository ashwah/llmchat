from typing import Any, Dict
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage, HumanMessage

class MultipersonConversationBufferMemory(ConversationBufferMemory):
    """Buffer for storing multiperson conversation memory."""

    name: str = "Bob"

    def set_name(self, name):
        self.name = name

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        """Save context from this conversation to buffer."""
        input_str, output_str = self._get_input_output(inputs, outputs)
        self.chat_memory.add_messages(
            [HumanMessage(content=input_str, name=self.name), AIMessage(content=output_str)]
        )

    async def asave_context(
        self, inputs: Dict[str, Any], outputs: Dict[str, str]
    ) -> None:
        """Save context from this conversation to buffer."""
        input_str, output_str = self._get_input_output(inputs, outputs)
        await self.chat_memory.aadd_messages(
            [HumanMessage(content=input_str, name=self.name), AIMessage(content=output_str)]
        )