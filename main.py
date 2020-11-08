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

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from nbt.nbt import NBTFile
import rapidjson as json

import sys
import os

import utils

try:
    DIRECTORY = sys._MEIPASS
except:
    DIRECTORY = os.path.dirname(__file__)

__version__ = open(os.path.join(DIRECTORY, "VERSION.txt")).read()

SETTINGS = QSettings(QSettings.NativeFormat, QSettings.UserScope, "Minecraft Automatic Advancements Checklist")


def get_last_played_level():
    mc_dir = SETTINGS.value("MinecraftDirectory", utils.get_default_minecraft_dir())
    mc_saves = os.path.join(mc_dir, "saves")

    worlds_recently_modified = sorted([os.path.join(mc_saves, s) for s in os.listdir(mc_saves)], key=os.path.getmtime, reverse=True)
    for world in worlds_recently_modified:
        try:
            level = NBTFile(os.path.join(world, "level.dat"))
            with open(os.path.join(world, "advancements", os.listdir(os.path.join(world, "advancements"))[0])) as f:
                advancements = dict(json.load(f))
            break
        except:
            continue

    data = {
        "name": str(level["Data"]["LevelName"]),
        "version": str(level["Data"]["Version"]["Name"]),
        "dataversion": int(str(level["Data"]["DataVersion"])),
        "adv": advancements
    }

    return data


class Tab(QWidget):
    def __init__(self, parent=None):
        super(Tab, self).__init__(parent)

        layout = QVBoxLayout()
        self.scroll_area = QScrollArea()
        self.list = QWidget()
        self.advancements = QVBoxLayout()
        self.list.setLayout(self.advancements)

        layout.addWidget(self.scroll_area)
        self.setLayout(layout)

        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.list)

    def reset_list(self):
        for i in reversed(range(self.advancements.count())):
            try:
                self.advancements.itemAt(i).widget().setParent(None)
            except:
                continue

        self.completion = QLabel("<b>Completion</b>: N/A")
        self.completion.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.advancements.addWidget(self.completion)


class CollapsibleBox(QWidget):
    def __init__(self, title="", parent=None):
        super(CollapsibleBox, self).__init__(parent)

        self.toggle_button = QToolButton(text=title)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setStyleSheet("QToolButton { border: none; }")
        self.toggle_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(Qt.RightArrow)
        self.toggle_button.toggled.connect(self.on_pressed)

        self.toggle_animation = QParallelAnimationGroup(self)

        self.content_area = QScrollArea(maximumHeight=0, minimumHeight=0)
        self.content_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.content_area.setFrameShape(QFrame.NoFrame)

        lay = QVBoxLayout(self)
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.toggle_button)
        lay.addWidget(self.content_area)

        self.toggle_animation.addAnimation(QPropertyAnimation(self, b"minimumHeight"))
        self.toggle_animation.addAnimation(QPropertyAnimation(self, b"maximumHeight"))
        self.toggle_animation.addAnimation(QPropertyAnimation(self.content_area, b"maximumHeight"))

    def on_pressed(self, checked):
        self.toggle_button.setArrowType(Qt.DownArrow if checked else Qt.RightArrow)
        self.toggle_animation.setDirection(QAbstractAnimation.Forward if checked else QAbstractAnimation.Backward)
        self.toggle_animation.start()

    def setContentLayout(self, layout):
        lay = self.content_area.layout()
        del lay

        self.content_area.setLayout(layout)
        collapsed_height = (self.sizeHint().height() - self.content_area.maximumHeight())
        content_height = layout.sizeHint().height()
        for i in range(self.toggle_animation.animationCount()):
            animation = self.toggle_animation.animationAt(i)
            animation.setDuration(500)
            animation.setStartValue(collapsed_height)
            animation.setEndValue(collapsed_height + content_height)

        content_animation = self.toggle_animation.animationAt(self.toggle_animation.animationCount() - 1)
        content_animation.setDuration(500)
        content_animation.setStartValue(0)
        content_animation.setEndValue(content_height)


class ChecklistWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Minecraft Automatic Advancements Checklist")
        if bool(int(SETTINGS.value("PinWindow", 0))):
            self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(os.path.join(DIRECTORY, "Resources", "icons.ico")))

        self.mc_version = None
        self.reset_on_next = False
        self.last_completion = {"total": -1, "minecraft": -1, "nether": -1, "end": -1, "adventure": -1, "husbandry": -1}

        self.widget_layout = QVBoxLayout()

        self.version_text = QLabel(f"v{__version__} (<a href='https://github.com/NinjaSnail1080/maac'>Github</a>)")
        self.version_text.linkActivated.connect(self.open_link)

        self.spacer = QWidget()
        self.spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.pin_button = QAction(QIcon(os.path.join(DIRECTORY, "Resources", "pin.png")), "Pin window", self)
        self.pin_button.setCheckable(True)
        self.pin_button.toggled.connect(self.pin_unpin_window)
        if bool(int(SETTINGS.value("PinWindow", 0))):
            self.pin_button.setChecked(True)

        self.settings_button = QAction(QIcon(os.path.join(DIRECTORY, "Resources", "folder.png")), "Change MC Directory", self)
        self.settings_button.triggered.connect(self.change_mc_dir)

        self.help_button = QAction(QIcon(os.path.join(DIRECTORY, "Resources", "help.png")), "Help", self)
        self.help_button.triggered.connect(self.open_help)

        self.toolbar = QToolBar("Main toolbar")
        self.toolbar.setIconSize(QSize(16, 16))
        self.toolbar.setMovable(False)
        self.toolbar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.toolbar.setStyleSheet("border: none;")
        self.toolbar.addWidget(self.version_text)
        self.toolbar.addWidget(self.spacer)
        self.toolbar.addAction(self.pin_button)
        self.toolbar.addAction(self.settings_button)
        self.toolbar.addAction(self.help_button)
        self.addToolBar(self.toolbar)

        self.world_name = QLabel("<b>World</b>:")
        self.world_name.setAlignment(Qt.AlignCenter)
        self.widget_layout.addWidget(self.world_name)

        self.version = QLabel("<b>Version</b>:")
        self.version.setAlignment(Qt.AlignCenter)
        self.widget_layout.addWidget(self.version)

        self.completion = QLabel("<b>Completion</b>: N/A")
        self.completion.setAlignment(Qt.AlignCenter)
        self.widget_layout.addWidget(self.completion)

        self.tabs_widget = QTabWidget()
        self.tabs = {"minecraft": Tab(), "nether": Tab(), "end": Tab(), "adventure": Tab(), "husbandry": Tab()}

        self.tabs_widget.addTab(self.tabs["minecraft"], "Minecraft")
        self.tabs_widget.addTab(self.tabs["nether"], "Nether")
        self.tabs_widget.addTab(self.tabs["end"], "The End")
        self.tabs_widget.addTab(self.tabs["adventure"], "Adventure")
        self.tabs_widget.addTab(self.tabs["husbandry"], "Husbandry")

        self.widget_layout.addWidget(self.tabs_widget)

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.widget_layout)
        self.setCentralWidget(self.main_widget)

        self.timer = QTimer()
        self.timer.setTimerType(Qt.PreciseTimer)
        self.timer.timeout.connect(self.update_adv)

        self.update_adv()

        try:
            self.resize(int(SETTINGS.value("SizeX", None)), int(SETTINGS.value("SizeY", None)))
        except:
            self.resize(self.main_widget.sizeHint())
        try:
            self.move(int(SETTINGS.value("PosX", None)), int(SETTINGS.value("PosY", None)))
        except:
            pass

        self.timer.start(100)
        self.show()

    def update_adv(self):
        try:
            level_data = get_last_played_level()
        except:
            self.world_name.setText("<b><font color='red'>ERROR: Couldn't Find Compatible World</font></b>")
            self.version.setText("<font color='red'>Make sure the Minecraft directory is correct and you're playing in 1.12+</font>")
            self.completion.setText("<b>Completion</b>: N/A")
            self.reset_on_next = True
            for tab in self.tabs.values():
                tab.reset_list()
            return

        self.world_name.setText(f"<b>World</b>: {level_data['name']}")
        self.version.setText(f"<b>Version</b>: {level_data['version']}")

        completion = {"total": 0, "minecraft": 0, "nether": 0, "end": 0, "adventure": 0, "husbandry": 0}

        adv_data = utils.get_adv_file(level_data["dataversion"], DIRECTORY)
        if adv_data is None:
            self.version.setText("<font color='red'>UNSUPPORTED VERSION (1.12 - 1.16.4 only)</font>")
            self.completion.setText("<b>Completion</b>: N/A")
            self.reset_on_next = True
            for tab in self.tabs.values():
                tab.reset_list()
            return

        if level_data["version"] != self.mc_version or self.reset_on_next:
            for cat, tab in self.tabs.items():
                tab.reset_list()
                for a, d in adv_data[cat].items():
                    box = CollapsibleBox(d["name"])
                    box.setToolTip(d["description"])
                    box_layout = QVBoxLayout()
                    for c in d["criteria"]:
                        if d["all"]:
                            label = QLabel(utils.UNCHECKED_BOX + c.replace("minecraft:", "").replace("textures/entity/cat/", "").replace(".png", ""))
                        else:
                            label = QLabel(utils.UNCHECKED_RADIO + c.replace("minecraft:", "").replace("textures/entity/cat/", "").replace(".png", ""))
                        box_layout.addWidget(label)
                    box.setContentLayout(box_layout)
                    tab.advancements.addWidget(box)
                tab.advancements.addStretch()
            self.reset_on_next = False

        self.mc_version = level_data["version"]

        for adv, data in level_data["adv"].items():
            if "/root" not in adv:
                if "minecraft:story" in adv:
                    completion_tab = "minecraft"
                    adv_dict = adv_data["minecraft"]
                    tab = self.tabs["minecraft"]
                elif "minecraft:nether" in adv:
                    completion_tab = "nether"
                    adv_dict = adv_data["nether"]
                    tab = self.tabs["nether"]
                elif "minecraft:end" in adv:
                    completion_tab = "end"
                    adv_dict = adv_data["end"]
                    tab = self.tabs["end"]
                elif "minecraft:adventure" in adv:
                    completion_tab = "adventure"
                    adv_dict = adv_data["adventure"]
                    tab = self.tabs["adventure"]
                elif "minecraft:husbandry" in adv:
                    completion_tab = "husbandry"
                    adv_dict = adv_data["husbandry"]
                    tab = self.tabs["husbandry"]
                else:
                    continue
            else:
                continue

            for i in reversed(range(tab.advancements.count())):
                try:
                    adv_box = tab.advancements.itemAt(i).widget()
                    if adv_box.toggle_button.text() == adv_dict[adv]["name"]:
                        if data["done"]:
                            adv_box.toggle_button.setStyleSheet("QToolButton { border: none; color: green; font-weight: bold; }")
                            completion["total"] += 1
                            completion[completion_tab] += 1
                        for c in adv_dict[adv]["criteria"]:
                            criteria_label = adv_box.content_area.layout().itemAt(adv_dict[adv]["criteria"].index(c)).widget()
                            if c in data["criteria"]:
                                if adv_dict[adv]["all"]:
                                    criteria_label.setText(utils.CHECKED_BOX + criteria_label.text()[3:])
                                else:
                                    criteria_label.setText(utils.CHECKED_RADIO + criteria_label.text()[3:])
                            else:
                                if adv_dict[adv]["all"]:
                                    criteria_label.setText(utils.UNCHECKED_BOX + criteria_label.text()[3:])
                                else:
                                    criteria_label.setText(utils.UNCHECKED_RADIO + criteria_label.text()[3:])
                        break
                except:
                    continue

        if completion['total'] == sum(len(d) for d in adv_data.values()):
            self.completion.setText(f"<font color='green'><b>Completion</b>: {completion['total']}/{sum(len(d) for d in adv_data.values())} ({round((completion['total'] / sum(len(d) for d in adv_data.values())) * 100, 2)}%)</font>")
        else:
            self.completion.setText(f"<b>Completion</b>: {completion['total']}/{sum(len(d) for d in adv_data.values())} ({round((completion['total'] / sum(len(d) for d in adv_data.values())) * 100, 2)}%)")
        for cat, tab in self.tabs.items():
            if completion[cat] == len(adv_data[cat]):
                tab.completion.setText(f"<font color='green'><b>Completion</b>: {completion[cat]}/{len(adv_data[cat])} ({round((completion[cat] / len(adv_data[cat])) * 100, 2)}%)</font>")
            else:
                tab.completion.setText(f"<b>Completion</b>: {completion[cat]}/{len(adv_data[cat])} ({round((completion[cat] / len(adv_data[cat])) * 100, 2)}%)")

        if any([completion[i] < self.last_completion[i] for i in completion]):
            self.reset_on_next = True
        self.last_completion = completion

    def open_link(self, link):
        QDesktopServices.openUrl(QUrl(link))

    def pin_unpin_window(self, checked):
        if checked:
            self.pin_button.setIcon(QIcon(os.path.join(DIRECTORY, "Resources", "unpin.png")))
            self.pin_button.setToolTip("Unpin Window")
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            SETTINGS.setValue("PinWindow", 1)
            self.show()
        else:
            self.pin_button.setIcon(QIcon(os.path.join(DIRECTORY, "Resources", "pin.png")))
            self.pin_button.setToolTip("Pin Window")
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
            SETTINGS.setValue("PinWindow", 0)
            self.show()

    def change_mc_dir(self):
        browse = QFileDialog(self)
        browse.setFileMode(QFileDialog.DirectoryOnly)
        if browse.exec_():
            mc_dir = browse.selectedFiles()[0]
            SETTINGS.setValue("MinecraftDirectory", mc_dir)

    def open_help(self):
        self.open_link("https://github.com/NinjaSnail1080/maac/blob/main/README.md")

    def closeEvent(self, *args, **kwargs):
        super(QMainWindow, self).closeEvent(*args, **kwargs)

        SETTINGS.setValue("SizeX", self.size().width())
        SETTINGS.setValue("SizeY", self.size().height())
        SETTINGS.setValue("PosX", self.x())
        SETTINGS.setValue("PosY", self.y())


if __name__ == "__main__":
    app = QApplication([])
    app.setStyle(QStyleFactory.create("Fusion"))

    window = ChecklistWindow()
    app.exec_()
    sys.exit()
