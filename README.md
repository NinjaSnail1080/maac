# Minecraft Automatic Advancements Checklist
**An open-source, cross-platform, easy-to-use tool for keeping track of your Minecraft advancements**

Copyright © 2020 NinjaSnail1080 (Discord User: @NinjaSnail1080#8581)

Licensed under the GNU General Public License v3.0. See LICENSE.txt for details

### [Download for your OS here](https://github.com/NinjaSnail1080/maac/releases) (Windows, MacOS, and Linux)

### For Minecraft versions 1.12 - 1.16.4

## Usage
This program reads from your most recent world's `advancements` file to see which advancements you've completed and which ones you have left.

Click the pin/unpin icon to pin/unpin the window. When unpinned, the window will behave like normal, but when pinned, it'll always remain on top of all the other windows.

Click the folder icon to set your Minecraft directory. By default, the program will read from the default Minecraft folder for your OS, but if use a different directory, you'll have to change it here.

Click the help icon to be directed to this page.

There are 5 tabs: Minecraft, Nether, The End, Adventure, and Husbandry, which correspond to the 5 different categories of advancements in the game. Each tab will display a list of the advancements in that category. The ones you have completed will be green and bold. At the top it will show you how many you have completed compared to the total and the percentage that you've completed.

Mouseover each advancment to display a tooltip that will explain its requirements. Click on it to expand a list of all the criteria that you must meet to achieve that advancment. Most only have one criterion.

If the criteria have checkboxes (`☐`/`☑`) next to them, then you must meet all of the criteria to complete the advancment. For instance, this is the case for `Monsters Hunted` (kill all hostile mobs) and `Adventuring Time` (visit every biome). If they have radio buttons instead (`○`/`⦿`), you only need to meet one of the criteria, which is the case for `Suit Up` (make any piece of iron armor) and `Fishy Business` (catch any type of fish).

The advancements checklist does not update in real time because the game only updates the advancements file when it saves. It will update every 5 minutes on autosaves, every time you open the pause menu, and when you go through the exit portal in the End.

If the checklist doesn't update when you make a new world, then there are two possibilities. One is that you migrated your Minecraft directory, but the old one still exists and that's where the program is reading from. Change your directory to the correct one by clicking on the folder icon in the top-right corner.

If you're playing in 1.16.2+, the Piglin Brute won't appear in the criteria list for `Monster Hunter` or `Monsters Hunted`, but you will have to kill one to get the latter advancment.

**Note**: There's a minor visual bug where the Completion text for each tab sometimes won't be aligned to the top of the box. Simply closing and reopening the application will fix it.

If you still experience issues or have any other questions, you can message me on Discord at NinjaSnail1080#8581 or [open an issue here](https://github.com/NinjaSnail1080/maac/issues).

---

That's about it. Good luck!