#!/usr/bin/env bash
# client_examples.sh
BASE="http://127.0.0.1:8000"

echo "Insert a student"
curl -s -X POST "$BASE/students" -H "Content-Type: application/json" \
  -d '{"name":"Lina Park","major":"AI","gpa":3.7}' | jq .

echo -e "\nList students with gpa >= 3.6"
curl -s "$BASE/students?gpa_min=3.6" | jq .

echo -e "\nShow raw parameterized query"
curl -s "$BASE/raw-query?gpa_min=3.6" | jq .

echo -e "\nShow unsafe/raw concatenation demo (do not use in prod)"
curl -s "$BASE/raw-query?gpa_min=3.6&unsafe=1" | jq .
