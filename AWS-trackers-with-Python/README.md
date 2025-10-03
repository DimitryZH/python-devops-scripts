# AWS Trackers

This folder contains small, single-purpose Python scripts that enumerate or "track" AWS resources across regions. The intent is to provide multiple approaches and examples (inventory snapshots, tag-based collectors, service-specific trackers like Amplify) that can be reused in SRE/DevOps workflows.

Conventions
- Folder name: `aws-trackers` — contains AWS-focused tracker scripts.
- Filenames: Use lowercase with underscores, e.g. `aws_resources.py`, `amplify_tracker.py`, `s3_inventory.py`.
- Each script should provide:
  - A function that performs the primary action (e.g. `list_all_resources()` or `get_amplify_apps()`).
  - An optional `save_to_json(data)` helper to store output with a timestamped filename.
  - A `if __name__ == "__main__"` block that runs a quick, safe example.

Dependencies
- Recommended: `boto3` for AWS SDK usage. Add any additional packages to `requirements.txt` in this folder.

Usage examples

Run the included inventory script (if present):

```powershell
python aws_resources.py
```

Add a new tracker
1. Create `amplify_tracker.py`.
2. Implement `get_amplify_apps(session, region)` or a similar function.
3. Add integration to `run_all.py` (if present) and document the new script in this README.

Notes
- These scripts should run using a configured AWS profile (default) or environment credentials.
- Keep each script focused and testable. If a script grows large, consider splitting service-specific helpers into modules.
