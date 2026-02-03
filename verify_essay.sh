#!/bin/bash
set -e

echo "Checking personas..."
PERSONAS=$(curl -s http://localhost:8000/personas/)

if [ "$PERSONAS" == "[]" ]; then
    echo "Creating persona..."
    curl -s -X POST http://localhost:8000/personas/ -H "Content-Type: application/json" -d '{"name": "Alice", "age": 30, "gender": "Female"}'
    PERSONA_ID=1
else
    # Extract first persona ID (assuming simple json structure or just use 1 if exists)
    # Using python to parse for safety
    PERSONA_ID=$(echo $PERSONAS | python3 -c "import sys, json; print(json.load(sys.stdin)[0]['id'])")
fi

echo "Using Persona ID: $PERSONA_ID"

echo "Triggering generation..."
JOB_RESPONSE=$(curl -s -X POST http://localhost:8000/essay/generate -H "Content-Type: application/json" -d "{\"persona_id\": $PERSONA_ID, \"starting_text\": \"The wind was howling outside properly.\"}")
echo "Job Response: $JOB_RESPONSE"

JOB_ID=$(echo $JOB_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['job_id'])")

echo "Polling for job $JOB_ID..."
for i in {1..30}; do
    STATUS_RES=$(curl -s http://localhost:8000/essay/status/$JOB_ID)
    STATUS=$(echo $STATUS_RES | python3 -c "import sys, json; print(json.load(sys.stdin)['status'])")
    echo "Status: $STATUS"
    
    if [ "$STATUS" == "finished" ]; then
        echo "Authentication Success!"
        RESULT=$(echo $STATUS_RES | python3 -c "import sys, json; print(json.load(sys.stdin)['result'])")
        echo "Result Sample: ${RESULT:0:100}..."
        exit 0
    elif [ "$STATUS" == "failed" ]; then
        echo "Job Failed!"
        echo $STATUS_RES
        exit 1
    fi
    sleep 2
done

echo "Timeout waiting for job."
exit 1
