# Smoke Tests

Run these from the project root.

## 1. Default text output
```bash
python3 access_review_helper.py docs/sample_access_list.csv
```

## 2. JSON output to terminal
```bash
python3 access_review_helper.py docs/sample_access_list.csv --format json
```

## 3. JSON output to file
```bash
python3 access_review_helper.py docs/sample_access_list.csv --format json --output docs/report.json
```

## 4. Bad path should fail (exit 1)
```bash
python3 access_review_helper.py docs/does_not_exist.csv || echo "expected failure"
```

## 5. Empty file should fail (exit 1)
```bash
: > docs/bad.csv
python3 access_review_helper.py docs/bad.csv || echo "expected failure"
rm docs/bad.csv
```

## 6. Check exit code for disabled privileged (sample data → exit 2)
```bash
python3 access_review_helper.py docs/sample_access_list.csv >/dev/null
echo $?
```
