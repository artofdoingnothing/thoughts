from libs.db_service import ConversationService, PersonaService, ThoughtService
from libs.processor_service import ProcessorService
from typing import List, Optional

class ConversationUseCases:
    def __init__(self):
        self.processor = ProcessorService()

    def generate_conversation_message(self, conversation_id: int, persona_id: int) -> List[str]:
        conversation = ConversationService.get_conversation(conversation_id)
        persona = PersonaService.get_persona(persona_id)
        
        if not conversation or not persona:
            return []

        sorted_messages = sorted(conversation.messages, key=lambda m: m.created_at)
        recent = sorted_messages[-5:]
        
        recent_messages_data = [
            {"persona": m.persona.name if m.persona else "Unknown", "content": m.content}
            for m in recent
        ]

        other_personas_info = ""
        for p in conversation.personas:
            if p.id != persona_id:
                other_personas_info += f"- Name: {p.name}, Age: {p.age}, Gender: {p.gender}\\n"
        
        if not other_personas_info:
            other_personas_info = "None"

        message_contents = self.processor.generate_conversation_message(
            persona_name=persona.name,
            persona_age=persona.age,
            persona_gender=persona.gender,
            persona_profile=persona.profile,
            conversation_context=conversation.context or conversation.title,
            recent_messages=recent_messages_data,
            other_personas_info=other_personas_info
        )
        
        for content in message_contents:
            ConversationService.add_message(
                conversation_id=conversation_id, 
                persona_id=persona_id, 
                content=content, 
                is_generated=True
            )
        return message_contents

    def process_conversation_thoughts(self, conversation_id: int):
        conversation = ConversationService.get_conversation(conversation_id)
        if not conversation:
            return
        
        for msg in conversation.messages:
            if not msg.persona_id:
                continue
            ThoughtService.create_thought(
                content=msg.content,
                persona_id=msg.persona_id,
                is_generated=msg.is_generated,
                thought_type="Conversation",
                # Ignore created_at for now, creation time will be generation time.
                # To maintain full parity we'd need to allow setting created_at in create_thought.
            )
