#!/usr/bin/python
# -*- coding:utf-8 -*-
# Small script to migrate configuration to new version

import os
import glob

from piblo.config_wrapper import Configs
from piblo.constants import ConfigConst


def extract_number(path):
    try:
        # assume everything after `_` is a number
        return int(path.rpartition('_')[-1])
    except ValueError:
        # not everything was a number, skip this directory
        return None


def backup_file(file_path):
    # Use glob to backup https://stackoverflow.com/questions/38885370/rename-backup-old-directory-in-python
    if os.path.exists(file_path):
        backups = glob.glob(file_path + '_[0-9]*')

        backup_numbers = (extract_number(b) for b in backups)
        try:
            next_backup = max(filter(None, backup_numbers)) + 1
        except ValueError:
            # no backup files
            next_backup = 1

    new_path = file_path + '_{:d}'.format(next_backup)

    os.rename(file_path, new_path)
    return new_path


# Start script
print("pycasso Configuration Migration Utility")

old_config = Configs(config_path=ConfigConst.CONFIG_PATH.value)

if old_config.does_config_file_exist():
    old_config.read_config()

    backup_path = backup_file(old_config.config_path)
    print(f"Config file exists. Backed up to {backup_path}")

    new_config = Configs(config_path=ConfigConst.CONFIG_PATH_EG.value)
    print(f"Migrating any new items from {new_config.config_path} to {old_config.config_path}")

    old_config.insert_config(new_config.read_config())
    old_config.write_config(old_config.config_path)
    print(f"Save complete")

else:
    print(f"File '{old_config.config_path}' didn't exist anyway. Proceeding with loading example configs.")
    new_config = Configs(config_path=ConfigConst.CONFIG_PATH.value,
                         example_config_path=ConfigConst.CONFIG_PATH_EG.value)
    print(f"Moving '{new_config.example_path}' to '{new_config.config_path}'")
    new_config.backup_config()

print("Closing pycasso Configuration Migration Utility")
