# Codex instructions for O'KeegSan

These instructions apply to the entire repository.

## Purpose

Maintain a clear, low-friction source of prompts and activity records for an
audio-chat exercise companion. Preserve the friendly “keep going” character
without presenting estimates as sensor measurements.

## Editing rules

- Keep reusable behavior in `modes/` and reusable schemas in `templates/`.
- Put completed logs only in `logs/<mode>/<YYYY>/`.
- Use local-date filenames: `YYYYMMDD_run_log.md`, `YYYYMMDD_wt_log.md`, and
  `YYYYMMDD_bike_log.md`.
- Never invent elapsed time, distance, heart rate, route, exercise, weight,
  repetitions, sources, or discussion topics. Mark unknown values `not recorded`.
- Preserve the user's wording in notes where practical, correcting only obvious
  transcription errors.
- Do not put credentials, access tokens, medical records, precise home addresses,
  or private location history in the repository.
- When adding a new activity mode, add its prompt, template, log folder, and root
  README entry in the same change.
- Prefer concise Markdown that is easy to read on a phone.

## Verification

Before committing, check `git diff --check`, confirm links and paths, and ensure
that no secrets or private location details were added.
