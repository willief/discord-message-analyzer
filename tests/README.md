# Discord Analyser Tests

This directory contains the test suite for Discord Analyser.

## Running Tests

```bash
cd ~/projects/discord_analyser
./tests/run_tests.sh
```

## Test Coverage

1. **Basic Digest Generation** - Verifies the core digest generation works
2. **Output File Creation** - Ensures all expected files are created
3. **JSON Structure** - Validates JSON output has correct structure
4. **Message Capture** - Verifies messages are being captured
5. **Interaction Types** - Checks all interaction types are detected
6. **Markdown Formatting** - Validates markdown output format

## Test Data

Test fixtures are in `tests/fixtures/` and include a minimal Discord export JSON with:

- User posts
- Replies
- Reactions
- Thread conversations

## Expected Results

All tests should pass with output files in `tests/output/`:

- `test_archive.md` - Markdown archive
- `test_weekly.md` - Markdown weekly digest
- `test_digest.json` - JSON digest with full context
-