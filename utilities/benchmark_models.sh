#!/bin/bash

SERVER_URL="http://192.168.1.60:11435/api/generate"
PROMPT="Explain the difference between artificial intelligence and artificial general intelligence in simple terms."
MODELS=("mistral:7b" "llama3:8b" "deepseek-r1:8b" "phi3:latest" "llama3.2:3b" "deepseek-r1:7b")

for model in "${MODELS[@]}"
do
    echo -e "\n🧪 Benchmarking model: $model"

    START_TIME=$(date +%s.%N)

    RESPONSE=$(curl -s -X POST "$SERVER_URL" \
        -H "Content-Type: application/json" \
        -d "{
            \"model\": \"$model\",
            \"prompt\": \"$PROMPT\",
            \"stream\": false
        }")

    END_TIME=$(date +%s.%N)
    DURATION=$(echo "$END_TIME - $START_TIME" | bc)

    TEXT=$(echo "$RESPONSE" | jq -r '.response // ""')
    TOKENS=$(echo "$TEXT" | jq -R 'split(" ") | length')

    echo "$TEXT" | fold -s -w 100

    echo -e "\n⏱️  Time taken: ${DURATION}s"
    echo -e "🔠 Tokens generated: $TOKENS"
    echo -e "🚀 Estimated tokens/sec: $(echo "$TOKENS / $DURATION" | bc -l | xargs printf "%.2f")"
done
