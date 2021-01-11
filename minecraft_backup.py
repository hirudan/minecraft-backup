import getpass
import json
import os
import re
import shutil

def archive_world(world_path, last_mtime, backup_path):
    temp_file_name = os.path.split(world_path)[1] + "__" + str(last_mtime)
    file_name = shutil.make_archive(temp_file_name, 'zip', world_path)
    shutil.move(file_name, backup_path)

def save_routine():
    config_file_name = "minecraft_backup_settings.json"
    backup_path = ""
    last_modified_times = []
    num_backups_per_world = 7
    save_file_dir = "C:\\Users\\$current_user$\\AppData\\Roaming\\.minecraft\\saves"
    config_data = {}

    # Read config file and load up settings
    try:
        with open(config_file_name, 'r') as config_file:
            config_data = json.loads(config_file.read())
        backup_path = config_data["backup_path"]
        last_modified_times = config_data["last_modified_times"]
        num_backups_per_world = config_data["num_backups_per_world"]
    except Exception as e:
        print(e)
        print("Error loading config data, terminating")

    # Enumerate worlds to check
    current_user = getpass.getuser()
    world_dir = save_file_dir.replace("$current_user$", current_user)
    # If no backup path was specified, drop backup in Minecraft's persistence directory
    if not backup_path:
        backup_path = world_dir
    world_list = []
    for item in os.listdir(world_dir):
        if os.path.isdir(os.path.join(world_dir,item)):
            world_list.append(item)

    # Iterate through each world and decide if we need to save it
    dat_file = "level.dat"
    for world in world_list:
        print(str("Checking world " + world + "..."))
        try:
            last_mtime = os.path.getmtime(os.path.join(world_dir, world, dat_file))
        except OSError:
            print(e)
            print("Could not access " + dat_file + " for world " + world + ". Continuing...")
            continue
        if world in last_modified_times and last_mtime == last_modified_times[world]:
            print("Last modified time for world " + world + " did not change, not saving")
            continue
        try:
            # Archive world and write last modified time to configs
            archive_world(os.path.join(world_dir, world), last_mtime, backup_path)
            last_modified_times[world] = last_mtime
            print("Successfully archived world " + world + ".")
        except Exception as e:
            print("Error archiving world " + world)
            print(e)

        # Delete saves above the num_backups_per_world limit, starting with the oldest
        regex = re.compile(world + '.*\\.zip$')
        save_files = [file for file in os.listdir(backup_path) if regex.match(file)]
        delete_file_count = len(save_files) - num_backups_per_world
        if(delete_file_count > 0):
            save_files.sort(key=lambda f: os.path.getmtime(os.path.join(backup_path, f)))
            for i in range(0, delete_file_count):
                os.remove(os.path.join(backup_path, save_files[i]))

    # Write modified times back to the config file
    config_data["last_modified_times"] = last_modified_times
    with open(config_file_name, 'w') as config_file:
        json.dump(config_data, config_file)

save_routine()
