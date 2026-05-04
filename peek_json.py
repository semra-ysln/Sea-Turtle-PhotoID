import json

with open('turtles-data/data/annotations.json', 'r') as f:
    data = json.load(f)
    print("First annotation:", data['annotations'][0])
