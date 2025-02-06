@echo off

pyinstaller --onefile --windowed --icon=logo.ico ^
--add-data "background.png;./" ^
--add-data "logo.ico;./" ^
--name "Lethal Mod Manager" mod_manager.py

pause