import os
import requests
import zipfile
import shutil
import subprocess
import winreg
import locale
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import threading
import time
import sys




# region CONFIG

MODLOADER_REPOSITORY_URL = "https://github.com/furkanaliunal/lethal-company-modloader.git"
MODPACK_REPOSITORY_URL = "https://github.com/furkanaliunal/lethal_company_mod_pack.git"
CURRENT_VERSION_URL = "https://github.com/furkanaliunal/Lethal-Company-Modloader/releases/download/Release-0.3/Lethal.Mod.Manager.exe"
UPDATE_CHECK_URL = "https://api.github.com/repos/furkanaliunal/Lethal-Company-Modloader/releases/latest"
STEAM_APP_ID = "1966720"


# region LOCALE
MESSAGES = {
    "tr": {
        "app_title" : "Furkis Mod Yükleyici",
        "app_button_update" : "Güncelle",
        "app_button_start" : "Oyunu Başlat",
        "app_selection_copied" : "Seçilen Satır Kopyalandı!",
        "git_install" : "Git kurulumu yapılıyor",
        "git_folder_not_found" : "Git bulunamadı",
        "git_installation_complete" : "Git kurulumu tamamlandı",
        "git_fetching_updates" : "Çekirdek kuruluyor",
        "git_cleaning_files" : "Oyun dosyaları temizleniyor",
        "git_update_completed" : "Çekirdek kurulumu tamamlandı",
        "starting_game": "Oyun başlatılıyor..",
        "game_found": "Oyun bulundu!",
        "game_exe_path_not_found": "Oyunun başlatıcısı(.exe) bulunamadı",
        "game_start_failed": "Oyun başlatılamadı.",
        "game_directory_path_not_found": "Oyun dizini bulunamadı.",
        "mods_file_not_found": "Ek paketler bulunamadı",
        "mod_already_updated": "{} zaten güncel.",
        "downloading": "{} indiriliyor...",
        "download_failed": "{} indirilemedi!",
        "download_progress": "İndirme ilerlemesi: {:.2f}%",
        "download_completed": "İndirme tamamlandı!",
        "extracting": "{} başarıyla indirildi. Çıkarılıyor...",
        "installed_successfully": "{} başarıyla yüklendi!",
        "mod_install_complete": "Mod yükleme işlemi tamamlandı!",
        "modloader_update_checking": "Furkis Mod Yükleyicisi Güncellesi Kontrol Ediliyor..",
        "modloader_update_available": "Furkis Mod Yükleyicisinin Güncellemesi Mevcut!",
        "modloader_update_download": "İndirme Bağlantısı:\n{}\n\nÇift tıklayarak metni kopyalayabilirsin",
        "modloader_uptodate": "Furkis Mod Yükleyicisi Güncel",
        "modpack_update_checking": "Mod Paketi Güncellesi Kontrol Ediliyor..",
        "modpack_update_available": "Mod Paketinin Güncellemesi Mevcut!",
        "modpack_update_download": "Güncelle tuşuna basarak güncellemeni alabilirsin",
        "modpack_uptodate": "Mod Paketi Güncel",
        "updates_checking": "Güncellemeler kontrol ediliyor..",
    },
    "en": {
        "app_title" : "Furkis Mod Loader",
        "app_button_update" : "Update",
        "app_button_start" : "Start Game",
        "app_selection_copied" : "Selected Line Copied!",
        "git_install" : "Installing Git",
        "git_folder_not_found" : "Git not found",
        "git_installation_complete" : "Git installation completed",
        "git_fetching_updates" : "Fetching updates",
        "git_cleaning_files" : "Cleaning game files",
        "git_update_completed" : "Update completed",
        "starting_game": "Starting the game..",
        "game_found": "Game found!",
        "game_exe_path_not_found": "Game launcher (.exe) not found",
        "game_start_failed": "Game failed to start.",
        "game_directory_path_not_found": "Game directory not found.",
        "mods_file_not_found": "Mods not found",
        "mod_already_updated": "{} is already up to date.",
        "downloading": "Downloading {}...",
        "download_failed": "Failed to download {}!",
        "download_progress": "Download progress: {:.2f}%",
        "download_completed": "Download completed!",
        "extracting": "{} downloaded successfully. Extracting...",
        "installed_successfully": "{} installed successfully!",
        "mod_install_complete": "Mod installation complete!",
        "modloader_update_checking": "Checking for Furkis Mod Loader updates..",
        "modloader_update_available": "Furkis Mod Loader update available!",
        "modloader_update_download": "Download link:\n{}\n\nDouble-click to copy",
        "modloader_uptodate": "Furkis Mod Loader is up to date",
        "modpack_update_checking": "Checking for Mod Pack updates..",
        "modpack_update_available": "Mod Pack update available!",
        "modpack_update_download": "Press the update button to install the latest version",
        "modpack_uptodate": "Mod Pack is up to date",
        "updates_checking": "Checking for updates..",
    },
    "nl": {
        "app_title" : "Furkis Mod Loader",
        "app_button_update" : "Bijwerken",
        "app_button_start" : "Spel Starten",
        "app_selection_copied" : "Geselecteerde regel gekopieerd!",
        "git_install" : "Git wordt geïnstalleerd",
        "git_folder_not_found" : "Git niet gevonden",
        "git_installation_complete" : "Git-installatie voltooid",
        "git_fetching_updates" : "Updates ophalen",
        "git_cleaning_files" : "Spelbestanden opruimen",
        "git_update_completed" : "Update voltooid",
        "starting_game": "Spel wordt gestart..",
        "game_found": "Spel gevonden!",
        "game_exe_path_not_found": "Spel launcher (.exe) niet gevonden",
        "game_start_failed": "Spel kon niet worden gestart.",
        "game_directory_path_not_found": "Spelmap niet gevonden.",
        "mods_file_not_found": "Mods niet gevonden",
        "mod_already_updated": "{} is al up-to-date.",
        "downloading": "{} wordt gedownload...",
        "download_failed": "{} kon niet worden gedownload!",
        "download_progress": "Downloadvoortgang: {:.2f}%",
        "download_completed": "Download voltooid!",
        "extracting": "{} is succesvol gedownload. Uitpakken...",
        "installed_successfully": "{} is succesvol geïnstalleerd!",
        "mod_install_complete": "Mod-installatie voltooid!",
        "modloader_update_checking": "Controleren op updates voor Furkis Mod Loader..",
        "modloader_update_available": "Update voor Furkis Mod Loader beschikbaar!",
        "modloader_update_download": "Downloadlink:\n{}\n\nDubbelklik om te kopiëren",
        "modloader_uptodate": "Furkis Mod Loader is up-to-date",
        "modpack_update_checking": "Controleren op updates voor Mod Pack..",
        "modpack_update_available": "Update voor Mod Pack beschikbaar!",
        "modpack_update_download": "Druk op de updateknop om de nieuwste versie te installeren",
        "modpack_uptodate": "Mod Pack is up-to-date",
        "updates_checking": "Controleren op updates..",
    }
}



# region UTILITIES


def get_system_language():
    lang, encoding = locale.getlocale()
    if lang.startswith("Turkish"): lang = "tr"
    elif lang.startswith("Dutch"): lang = "nl"
    else: lang = "en"
    return lang



def check_git():
    try:
        subprocess.run(["git", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, creationflags=CREATION_FLAGS)
        return True
    except subprocess.CalledProcessError:
        return False

def install_git():
    if not check_git():
        APP.write_to_text_area(MSG["git_install"])
        subprocess.run(["winget", "install", "--id", "Git.Git", "-e", "--source", "winget"], shell=True, creationflags=CREATION_FLAGS)
    APP.write_to_text_area(MSG["git_installation_complete"])

def fetch_origin_and_reset_local_repo(game_dir, repo_url=MODPACK_REPOSITORY_URL):
    os.chdir(game_dir)
    
    if not os.path.exists(os.path.join(game_dir, ".git")):
        APP.write_to_text_area(MSG["git_folder_not_found"])
        subprocess.run(["git", "init"], shell=True, creationflags=CREATION_FLAGS)
        subprocess.run(["git", "remote", "add", "origin", repo_url], shell=True, creationflags=CREATION_FLAGS)
    
    APP.write_to_text_area(MSG["git_fetching_updates"])
    subprocess.run(["git", "fetch", "origin", "main", "no-mod", "--depth=1"], shell=True, creationflags=CREATION_FLAGS) 
    subprocess.run(["git", "reset", "--hard", "origin/main"], shell=True, creationflags=CREATION_FLAGS)

    
    APP.write_to_text_area(MSG["git_cleaning_files"])
    
    subprocess.run(["git", "clean", "-fd"], shell=True, creationflags=CREATION_FLAGS)
    
    APP.write_to_text_area(MSG["git_update_completed"])

def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)


def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)



# region GLOBAL VARIABLES

LANG = get_system_language()
MSG = MESSAGES[LANG]
APP = None
CREATION_FLAGS = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0




# region APPLICATION

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.init_variables()
        self.build_gui()

        threading.Thread(target=self.check_updates).start()

    def init_variables(self):

        self.game_path = self.find_game_directory()
        self.game_exe_path = self.find_game_directory(is_exe_path=True)
        self.external_mods_file = os.path.join(self.game_path, "external_mods.txt")
        self.external_mods_path = os.path.join(self.game_path, "BepInEx", "plugins", "externals")
        self.installed_mods_file = os.path.join(self.game_path, "installed_mods.txt")
        self.installed_mods = self.read_installed_mods()
        pass


    def build_gui(self):
        self.title(MSG["app_title"])
        self.geometry("600x400")
        self.resizable(False, False)
        self.iconbitmap(get_resource_path("logo.ico"))
        
        self.attributes('-alpha', 0.95)

        self.bg_image = Image.open(get_resource_path("background.png"))
        self.bg_image = self.bg_image.resize((600, 400))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = tk.Label(self, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        

        # text_frame = tk.Frame(self, bg="#2c2f33")
        self.text_frame = tk.Frame(self, bg="")
        self.text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 60))

        self.copy_label = tk.Label(self, text="", fg="green", bg="#23272a", font=("Arial", 10, "bold"))
        self.copy_label.pack(pady=5, before=self.text_frame)
        

        self.text_area = scrolledtext.ScrolledText(self.text_frame, wrap=tk.WORD, height=10, bg="#23272a", fg="white")
        self.text_area.bind("<Button-1>", self.highlight_line)
        self.text_area.bind("<Double-Button-1>", self.copy_selected_text)
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.text_area.tag_configure("gray", foreground="gray")
        self.text_area.tag_configure("red", foreground="red")
        self.text_area.tag_configure("green", foreground="green")
        

        self.update_button = tk.Button(self, text=MSG["app_button_update"], command=self.update_action, height=2, width=12)
        self.update_button.place(x=200, y=350)

        self.start_button = tk.Button(self, text=MSG["app_button_start"], command=self.start_action, height=2, width=12)
        self.start_button.place(x=320, y=350)

    def copy_selected_text(self, event):
        try:
            self.text_area.tag_remove("sel", "1.0", tk.END) 
            self.text_area.tag_add("sel", "current linestart", "current lineend")
            
            selected_text = self.text_area.get("sel.first", "sel.last")
            
            if selected_text:  
                self.clipboard_clear()
                self.clipboard_append(selected_text)
                self.update_idletasks()
                self.copy_label.config(text=MSG["app_selection_copied"], fg="green")
                self.after(2000, lambda: self.copy_label.config(text=""))
        except tk.TclError:
            pass

    def highlight_line(self, event):
        self.text_area.tag_remove("highlight", "1.0", tk.END)
        current_line = self.text_area.index(tk.CURRENT).split(".")[0]
        line_start = f"{current_line}.0"
        line_end = f"{current_line}.end"
        self.text_area.tag_add("highlight", line_start, line_end)
        self.text_area.tag_configure("highlight", background="green", foreground="black")
        # self.after(1000, lambda: self.text_area.tag_remove("highlight", line_start, line_end))

    def write_to_text_area_from_async(self, messages, color=None):
        self.after(0, self.write_to_text_area, messages, color)

    def write_to_text_area(self, messages, color=None):
        self.text_area.config(state=tk.NORMAL)
        if isinstance(messages, str):
            self.text_area.insert(tk.END, f"{messages}\n", color)
        else:
            for message in messages:
                self.text_area.insert(tk.END, f"{message}\n", color)
        self.text_area.see(tk.END)
        self.text_area.config(state=tk.DISABLED)

    def write_to_text_area_last_row(self, message, color=None):
        self.text_area.config(state=tk.NORMAL)
        lines = self.text_area.get("1.0", tk.END).splitlines()
        if lines:
            lines[-1] = message
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", "\n".join(lines))
        else:
            self.text_area.insert(tk.END, message)
        self.text_area.see(tk.END)
        self.text_area.update_idletasks()
        self.text_area.config(state=tk.DISABLED)

    def start_action(self):
        if not self.game_exe_path:
            self.write_to_text_area(MSG["game_exe_path_not_found"], "red")
            return
        self.write_to_text_area(MSG["game_found"])
        try:
            self.write_to_text_area(MSG["starting_game"])
            subprocess.Popen(["start", f"steam://run/{STEAM_APP_ID}"], shell=True, creationflags=CREATION_FLAGS)
        except Exception as e:
            self.write_to_text_area(MSG["game_start_failed"].format(e), "red")


    def update_action(self):
        if not self.game_path:
            self.write_to_text_area(MSG["game_directory_path_not_found"], "red")
            return
        install_git()
        fetch_origin_and_reset_local_repo(self.game_path)
        self.clean_external_mods()

        thread = threading.Thread(target=self.install_external_mods(), daemon=True)
        thread.start()



    def find_game_directory(self, is_exe_path = False, search_value = "Lethal Company"):
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "System\\GameConfigStore\\Children")
        for i in range(0, winreg.QueryInfoKey(reg_key)[0]):
            subkey_name = winreg.EnumKey(reg_key, i)
            subkey = winreg.OpenKey(reg_key, subkey_name)
            try:
                exe_parent_dir = winreg.QueryValueEx(subkey, "ExeParentDirectory")[0]
                if "Lethal Company".lower() in exe_parent_dir.lower():
                    matched_exe_full_path = winreg.QueryValueEx(subkey, "MatchedExeFullPath")[0]
                    if is_exe_path:
                        return matched_exe_full_path
                    return os.path.dirname(matched_exe_full_path)
            except FileNotFoundError:
                continue
        return None



    def clean_external_mods(self):

        self.installed_mods = self.read_installed_mods()
        if os.path.exists(self.external_mods_file):
            with open(self.external_mods_file, "r", encoding="utf-8") as f:
                allowed_mods = {line.split(";")[0].strip() for line in f if line.strip()}
        else:
            allowed_mods = set()


        installed_mods_to_remove = {mod for mod in self.installed_mods if mod not in allowed_mods}
        folders_to_remove = {folder for folder in os.listdir(self.external_mods_path) if folder not in allowed_mods}


        for folder in folders_to_remove:
            shutil.rmtree(os.path.join(self.external_mods_path, folder))
        for mod_to_remove in installed_mods_to_remove:
            self.installed_mods.pop(mod_to_remove)

        self.write_installed_mods()

    def install_external_mods(self):
        self.installed_mods = self.read_installed_mods()
        if not os.path.exists(self.external_mods_path):
            os.makedirs(self.external_mods_path)
        
        if not os.path.exists(self.external_mods_file):
            self.write_to_text_area(MSG["mods_file_not_found"])
            return

        with open(self.external_mods_file, "r") as f:
            for line in f:
                parts = line.strip().split(";")
                if len(parts) != 3:
                    continue
                
                mod_name, version, url = parts
                mod_path = os.path.join(self.external_mods_path, mod_name)
                
                if mod_name in self.installed_mods and self.installed_mods[mod_name] == version:
                    self.write_to_text_area(MSG["mod_already_updated"].format(mod_name))
                    continue
                
                self.write_to_text_area(MSG["downloading"].format(mod_name))
                zip_path = os.path.join(self.game_path, f"{mod_name}.zip")
                
                response = requests.get(url, stream=True)
                total_size = int(response.headers.get('content-length', 0))
                downloaded_size = 0
                if response.status_code == 200:
                    with open(zip_path, "wb") as f:
                        for chunk in response.iter_content(chunk_size=65536):
                            if chunk:
                                f.write(chunk)
                                downloaded_size += len(chunk) 
                                    
                                if total_size > 0:
                                    percent_complete = (downloaded_size / total_size) * 100
                                    self.write_to_text_area_last_row(f"İndirme ilerlemesi: %{percent_complete:.2f}")
                    self.write_to_text_area(MSG["download_completed"])
                    self.write_to_text_area(MSG["extracting"].format(mod_name))
                            
                    if os.path.exists(mod_path):
                        shutil.rmtree(mod_path)
                        os.makedirs(mod_path)
                    extract_zip(zip_path, mod_path)
                    os.remove(zip_path)
                    self.installed_mods[mod_name] = version
                    self.write_to_text_area(MSG["installed_successfully"].format(mod_name))

                else:
                    self.write_to_text_area(MSG["download_failed"].format(mod_name), "red")

        self.write_installed_mods()
        self.write_to_text_area(MSG["mod_install_complete"])


    def read_installed_mods(self):
        installed_mods = {}
        if os.path.exists(self.installed_mods_file):
            with open(self.installed_mods_file, "r") as f:
                for line in f:
                    parts = line.strip().split(";")
                    if len(parts) == 2:
                        installed_mods[parts[0]] = parts[1]
        return installed_mods

    def write_installed_mods(self):
        with open(self.installed_mods_file, "w") as f:
            for mod_name, version in self.installed_mods.items():
                f.write(f"{mod_name};{version}\n")

    def check_for_modloader_updates(self):
        response = requests.get(UPDATE_CHECK_URL)
        result = False, CURRENT_VERSION_URL
        if response.status_code == 200:
            release = response.json()
            asset_url = release['assets'][0]['browser_download_url']
            asset_id = release['assets'][0]['id']
            download_url = asset_url
            if download_url != CURRENT_VERSION_URL:
                result = True, download_url
        return result

    def print_modloader_update_status(self):
        self.write_to_text_area_from_async(MSG["modloader_update_checking"])
        is_available, url = self.check_for_modloader_updates()
        if is_available:
            self.write_to_text_area_from_async(MSG["modloader_update_available"])
            self.write_to_text_area_from_async(MSG["modloader_update_download"].format(url), "green")
        else:
            self.write_to_text_area_from_async(MSG["modloader_uptodate"], "gray")


    def check_for_modpack_updates(sef):

        # local commit
        local_commit_hash = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, creationflags=CREATION_FLAGS)
        if local_commit_hash.returncode == 0:
            local_commit_hash = local_commit_hash.stdout.strip()
        else:
            return False
        # remote commit
        remote_commit_hash = subprocess.run(["git", "ls-remote", "origin", "main"], capture_output=True, text=True, creationflags=CREATION_FLAGS)
        if remote_commit_hash.returncode == 0:
            remote_commit_hash = remote_commit_hash.stdout.split()[0]
        else:
            return False
        
        if local_commit_hash is None or remote_commit_hash is None:
            return False
        
        if local_commit_hash != remote_commit_hash:
            return True
        else:
            return False



    def print_modpack_update_status(self):
        self.write_to_text_area_from_async(MSG["modpack_update_checking"])
        if self.check_for_modpack_updates():
            self.write_to_text_area_from_async(MSG["modpack_update_available"])
            self.write_to_text_area_from_async(MSG["modpack_update_download"], "green")
        else:
            self.write_to_text_area_from_async(MSG["modpack_uptodate"], "gray")

    def check_updates(self):
        self.write_to_text_area_from_async(MSG["updates_checking"])
        self.print_modloader_update_status()
        self.print_modpack_update_status()

        

def main():
    global APP
    APP = App()
    APP.mainloop()
        

if __name__ == "__main__":
    main()
    
