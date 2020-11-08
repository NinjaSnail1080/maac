"""
    Minecraft Automatic Advancements Checklist
    Copyright (C) 2020  NinjaSnail1080  (Discord User: @NinjaSnail1080#8581)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import rapidjson as json

import sys
import os

CHECKED_BOX = "☑  "
UNCHECKED_BOX = "☐  "
CHECKED_RADIO = "⦿  "
UNCHECKED_RADIO = "○  "


def get_default_minecraft_dir():
    if sys.platform == "win32":
        return os.path.join(os.environ["APPDATA"], ".minecraft")
    elif sys.platform == "darwin":
        return os.path.expanduser("~/Library/Application Support/minecraft/")
    else:
        return os.path.expanduser("~/.minecraft/")


def get_adv_file(data_version, directory):
    adv_files = os.path.join(directory, "Resources", "adv_files")

    if 1139 <= data_version <= 1343:
        with open(os.path.join(adv_files, "12.json")) as f:
            return dict(json.load(f))
    elif 1519 <= data_version <= 1631:
        with open(os.path.join(adv_files, "13.json")) as f:
            return dict(json.load(f))
    elif 1952 <= data_version <= 1976:
        with open(os.path.join(adv_files, "14.json")) as f:
            return dict(json.load(f))
    elif 2225 <= data_version <= 2230:
        with open(os.path.join(adv_files, "15.json")) as f:
            return dict(json.load(f))
    elif 2566 <= data_version <= 2584:
        with open(os.path.join(adv_files, "16.json")) as f:
            return dict(json.load(f))
    else:
        return None
