# minecraft-backup
Python script to back up Minecraft worlds. Intended to be run by a scheduler.

## Purpose
After suffering an embarrassing death on my way back to base with an inventory full of rare ores and then dying again before I could recover them, I wished I could roll my game world back to the beginning of the session to wipe out such a major setback. Perhaps you've found yourself in a similar position. This script can be configured to back up your worlds on a regular basis so that you can fall back to a previous snapshot when the need arises.

## Dependencies
- Python 3
- Windows OS (for now)

## Usage
- Place script and settings file in a convenient location.
- In the settings file, modify the following:
-- `backup_path` to the location you want to save to (defaults to Minecraft save directory if blank)
-- `num_backups_per_world` to the number of snapshots you want to keep of a given world (default is 7).
- Either run the script via command line or set up a task via the Windows Task Scheduler to run the script at set intervals (recommended).
- To restore a snapshot, simply unzip a given backup and overwrite the world's directory in the Minecraft saves folder.

## Notes
- When the number of backups for a given world exceeds `num_backups_per_world` as specified in the config, the oldest backup for that world will be deleted.
- Save file contents are not modified.
- Avoid modifying `last_modified_times` in the config file; this setting is used to determine whether or not to back a world up based on the last time it was played. The script will not back up a world if there has been no play activity on it since the last backup.
