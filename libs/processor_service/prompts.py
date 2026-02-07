
COGNITIVE_DISTORTION_PROMPT = """
You are a mental health assistant expert in Cognitive Behavioral Therapy (CBT).
Analyze the following thought for Cognitive Distortions based on David Burns' definitions.
Identify any distortions present. If none are found, return an empty list.
Return the result strictly as a Python list of strings. Do not include any other text or explanation.

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
Return the result strictly as a Python list of strings. Do not include any other text or explanation.

Examples of emotions: Happy, Sad, Angry, Anxious, Fearful, Disgusted, Surprised, Neutral, Hopeful, Frustrated.

Thought: "{thought_content}"

Output format: ["Emotion 1", "Emotion 2"]
"""

THOUGHT_GENERATION_PROMPT = """
You are an AI assistant helping to extract thoughts from a blog post.
Analyze the following text content from a blog post and extract distinct thoughts expressed by the author.
A "thought" is a specific idea, opinion, or reflection.
Constraints:
- Extract at most 7 thoughts.
- Each thought must be under 2 sentences.
- Do not format the content or wording of the thoughts (no bullet points in the string itself, just the raw text).
- Return the result strictly as a Python list of strings. Do not include any other text or explanation.

Blog Content:
"{blog_content}"

Output format: ["Thought 1", "Thought 2"]
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
