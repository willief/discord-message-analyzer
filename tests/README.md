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
- ## End-to-End Tests

End-to-end tests verify the complete workflow including Discord export:
```bash
./tests/e2e_test.sh
```

### E2E Test Coverage

1. **DiscordChatExporter** - Verifies tool exists and is executable
2. **Token Security** - Checks token file permissions
3. **Fixture Processing** - Tests with sample data (always runs)
4. **Real Export** - Exports 1 day from real Discord (requires token)
5. **Real Data Processing** - Processes actual Discord exports
6. **Script Validation** - Syntax checks on automation scripts
7. **Autonomi CLI** - Checks for upload capability

### Running with Discord Token

To enable real Discord API tests, set up your token:
```bash
mkdir -p ~/.discord
chmod 700 ~/.discord
echo "YOUR_TOKEN"  
chmod 600 ~/.discord/token
```

### Skipped Tests

If no token is found, E2E tests will skip:
- Real Discord exports
- Real data processing

All other tests will still run.