
#!/bin/bash
# Count .txt files in data directory (any depth) and print the number
count=$(find ./data -type f -name '*.txt' 2>/dev/null | wc -l)
echo "$count"

