# 🎉 Changes Made - Outputs Now Go to outputs/ Directory

## What Changed

The script now automatically creates an `outputs/` directory and writes all generated files there by default.

## Before (Old Behavior):
```
~/projects/discord_analyser/
├── discord_digest.py
├── digests/
├── user_complete_archive.html     ← Files scattered in project root
├── user_complete_archive.md
├── user_digest.json
└── user_weekly_digest.md
```

## After (New Behavior):
```
~/projects/discord_analyser/
├── discord_digest.py
├── html_generator.py
├── digests/
└── outputs/                        ← All files organized here!
    ├── user_complete_archive.html
    ├── user_complete_archive.md
    ├── user_digest.json
    └── user_weekly_digest.md
```

## Usage (No Changes Required!)

Just run the same command:
```bash
python3 discord_digest.py --exports ./digests --username "dirvine."
```

The script will:
1. ✅ Automatically create `outputs/` directory if it doesn't exist
2. ✅ Write all files to `outputs/`
3. ✅ Keep your project root clean!

## Custom Output Location (Still Works)

You can still specify custom paths:
```bash
python3 discord_digest.py \
  --exports ./digests \
  --username "dirvine." \
  --archive-output my_custom_folder/archive.md \
  --json-output my_custom_folder/data.json
```

## Files Generated

All in `outputs/` directory:
- `user_complete_archive.md` - Markdown archive
- `user_complete_archive.html` - Beautiful HTML (open this!)
- `user_digest.json` - JSON for AI analysis
- `user_weekly_digest.md` - Last 7 days

## Benefits

✅ **Organized** - All outputs in one place
✅ **Clean** - Project root stays tidy
✅ **Automatic** - No manual folder creation needed
✅ **Flexible** - Can still use custom paths if needed

---

**Ready to use!** Just download the updated files and run the command.
