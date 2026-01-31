
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
