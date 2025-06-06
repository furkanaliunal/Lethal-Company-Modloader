@echo off

pyinstaller --onefile --windowed --icon=logo.ico ^
--add-data "src/background.png;./src" ^
--add-data "src/settings.png;./src" ^
--add-data "src/directory.png;./src" ^
--add-data "src/toggle_button_on.png;./src" ^
--add-data "src/toggle_button_off.png;./src" ^
--add-data "logo.ico;./" ^
--name "Lethal Mod Manager" mod_manager.py

pause