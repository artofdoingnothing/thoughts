
COGNITIVE_DISTORTION_PROMPT = """
You are a mental health assistant expert in Cognitive Behavioral Therapy (CBT).
Analyze the following thought for Cognitive Distortions based on David Burns' definitions.
Identify any distortions present. If none are found, return an empty list.
Return the result strictly as a valid JSON list of strings. Do not include any other text or explanation.

Known distortions:
- All-or-nothing thinking
- Overgeneralization
- Mental filter
- Disqualifying the positive
- Jumping to conclusions (Mind reading, Fortune telling)
- Magnification (Catastrophizing) or Minimization
- Emotional reasoning
- Should statements
- Labeling and mislabeling
- Personalization

Thought: "{thought_content}"

Output format: ["Distortion 1", "Distortion 2"]
"""

SENTIMENT_ANALYSIS_PROMPT = """
You are an expert in emotion analysis.
Analyze the following thought and identify the primary emotions associated with it.
Return the result strictly as a valid JSON list of strings. Do not include any other text or explanation.

Examples of emotions: Happy, Sad, Angry, Anxious, Fearful, Disgusted, Surprised, Neutral, Hopeful, Frustrated.

Thought: "{thought_content}"

Output format: ["Emotion 1", "Emotion 2"]
"""

TOPIC_ANALYSIS_PROMPT = """
You are an expert content analyzer.
Analyze the following thought and identify up to 3 main topics discussed.
Return the result strictly as a valid JSON list of strings. Do not include any other text or explanation.

Thought: "{thought_content}"

Output format: ["Topic 1", "Topic 2", "Topic 3"]
"""

THOUGHT_GENERATION_PROMPT = """
You are an AI assistant helping to extract thoughts from a blog post.
Analyze the following text content from a blog post and extract distinct thoughts expressed by the author.
A "thought" is a specific idea, opinion, or reflection.

Constraints:
- Extract complete thoughts or small paragraphs.
- Do not split a single coherent thought into multiple small sentences.
- Capture the full context of the thought.
- Return the result strictly as a valid JSON list of strings. Do not include any other text or explanation.

Blog Content:
"{blog_content}"

Output format: ["Thought 1 content...", "Thought 2 content..."]
"""

ESSAY_GENERATION_PROMPT = """
You are a creative writer.
Complete the following essay based on the starting text provided.
Adopt the persona described below.
Incorporating the provided emotions and tags into the tone and content of the essay.

Persona:
{persona_details}

Top Emotions: {emotions}
Top Tags: {tags}

Constraints:
- Continue the essay from the starting text.
- Maximum 500 words.
- Maintain the persona's voice.
- The written text should contain the emotions and tags provided together. Do not use the original tone of the provided text.
- Do not include the mentioned emotions and tags in the written text.
- Return only the completion text. Do not repeat the starting text unless necessary for flow, but preferably just continue.

Starting Text:
"{starting_text}"
"""

ACTION_ORIENTATION_PROMPT = """
You are a behavioral psychologist.
Analyze the following thought and classify it as either "Action-oriented" or "Ruminative".
"Action-oriented" thoughts focus on planning, problem-solving, or taking steps forward.
"Ruminative" thoughts focus on repetitive dwelling on negative feelings, past events, or abstract problems without a solution.

Return the result strictly as a single string: "Action-oriented" or "Ruminative". Do not include any other text or explanation.

Thought: "{thought_content}"

Output:
"""

THOUGHT_TYPE_PROMPT = """
You are a cognitive psychologist.
Analyze the following thought and classify it as either "Automatic" or "Deliberate".
"Automatic" thoughts are spontaneous, often habitual, and pop up without conscious effort.
"Deliberate" thoughts are conscious, intentional, and require effortful processing.

Return the result strictly as a single string: "Automatic" or "Deliberate". Do not include any other text or explanation.

Thought: "{thought_content}"

Output:
"""

ESSAY_DRAFT_AND_TAG_PROMPT = """
You are a creative writer.
Complete the following essay based on the starting text provided.
Adopt the persona described below.
Incorporating the provided thought type and action orientation into the tone and content of the essay.

Persona:
{persona_details}

Thought Type: {thought_type}
Action Orientation: {action_orientation}

Constraints:
- Continue the essay from the starting text.
- Maximum 500 words.
- Maintain the persona's voice.
- The written text should reflect the thought type and action orientation provided.
- Return the result strictly as a valid JSON object with two keys: "essay" (string) and "tags" (list of strings).
- "essay": The completed essay text. Ensure all newlines are escaped as \\n. Do not use literal newlines within the string.
- "tags": A list of 3-5 keywords or themes representing the content of the essay.

Starting Text:
"{starting_text}"

Output format:
{{
    "essay": "...",
    "tags": ["tag1", "tag2", "tag3"]
}}
"""

ESSAY_MODIFICATION_PROMPT = """
You are a creative editor.
Refine the following essay by infusing it with specific emotions.
The goal is to subtlety shift the tone of the essay to reflect these emotions without changing the core narrative or length significantly.

Emotions to infuse: {emotions}

Essay:
"{essay_content}"

Constraints:
- Return only the modified essay text.
- Do not add any preamble or explanation.
- Keep the length approximately the same.
"""

PROFILE_EMOTION_EXTRACTION_PROMPT = """
You are an expert psychological profiler.
Analyze the following "Starting Text" of an essay.
Compare it against the provided "Persona Profile" (which contains topics and associated emotions).
Identify which topic in the profile is most relevant to the starting text.
Extract the emotions associated with that topic.

Persona Profile:
{profile_json}

Starting Text:
"{starting_text}"

Return the result strictly as a valid JSON list of strings containing the emotions.
If no specific topic matches well, return the emotions from the most generic or first topic in the profile.

Output format: ["Emotion1", "Emotion2"]
"""

ESSAY_COMPLETION_FROM_PROFILE_PROMPT = """
You are a creative writer.
Complete the following essay based on the starting text provided.
Adopt the persona described below.
The essay should reflect the emotions and topics found in the persona's profile that are relevant to the text.

Persona:
{persona_details}

Relevant Emotions: {emotions}

Constraints:
- Continue the essay from the starting text.
- Maximum 500 words.
- Maintain the persona's voice.
- Seamlessly integrate the emotions into the narrative tone.
- Return only the completion text. Do not repeat the starting text unless necessary for flow.

Starting Text:
"{starting_text}"
"""

CONVERSATION_MESSAGE_GENERATION_PROMPT = """
You are roleplaying as a specific persona in a conversation.
Your goal is to contribute to the conversation naturally, staying in character.

Persona Details:
Name: {persona_name}
Age: {persona_age}
Gender: {persona_gender}
Profile: {persona_profile}

Other Personas in Conversation:
{other_personas_info}

Conversation Context:
{conversation_context}

Recent Messages:
{recent_messages}

Constraints:
- Respond as {persona_name} (Age: {persona_age}, Gender: {persona_gender}).
- Keep the response extremely concise, between 15-25 words.
- Respond as the persona would at their given age of {persona_age}.
- Reflect the persona's characteristics and emotions from their profile.
- Do NOT include the persona name at the start of the message. Just the message content.
"""
