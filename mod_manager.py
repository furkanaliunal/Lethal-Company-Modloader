import os
import requests
import zipfile
import shutil
import subprocess
import winreg
import locale




# region CONFIG

REPOSITORY_URL = "https://github.com/furkanaliunal/lethal_company_mod_pack.git"


# region LOCALE

MESSAGES = {
    "tr": {
        "git_installation_complete": "Git yükleme işlemi tamamlandı!",
        "git_folder_not_found": ".git klasörü bulunamadı. Depo başlatılıyor...",
        "cleaning_files": "Gereksiz dosyalar temizleniyor...",
        "game_directory_not_found": "Lethal Company dizini bulunamadı. Çıkılıyor...",
        "download_progress": "İndirme ilerlemesi: {:.2f}%",
        "download_complete": "İndirme tamamlandı!",
        "mods_file_not_found": "external_mods.txt bulunamadı!",
        "game_not_found": "Oyun bulunamadı! Çıkış yapılıyor...",
        "starting_game": "Oyun başlatılıyor...",
        "game_start_failed": "Oyun başlatılamadı: {}",
        "fetching_updates": "Güncellemeler alınıyor...",
        "update_completed": "Güncelleme işlemi tamamlandı!",
        "installing_git": "Git yükleniyor...",
        "installation_completed": "Kurulum tamamlandı!",
        "mod_already_updated": "{} zaten güncel.",
        "downloading": "{} indiriliyor...",
        "download_failed": "{} indirilemedi!",
        "extracting": "{} başarıyla indirildi. Çıkarılıyor...",
        "installed_successfully": "{} başarıyla yüklendi!",
        "mod_install_complete": "Mod yükleme işlemi tamamlandı!",
        "menu": """
        =======================================
              FurkisPack Yönetim Aracı
        =======================================
        1. Oyunu Başlat
        2. FurkisPack Yükle & Güncelle
        3. Çıkış
        =======================================
        """,
        "enter_choice": "Seçiminizi girin [1-3]: ",
        "invalid_choice": "Geçersiz seçim! Lütfen tekrar deneyin.",
        "press_enter": "Devam etmek için enter tuşuna basın"
    },
    "en": {
        "git_installation_complete": "Git installation completed!",
        "git_folder_not_found": ".git folder not found. Initializing repository...",
        "cleaning_files": "Cleaning up unnecessary files...",
        "game_directory_not_found": "Failed to locate Lethal Company directory. Exiting...",
        "download_progress": "Download progress: {:.2f}%",
        "download_complete": "Download complete!",
        "mods_file_not_found": "external_mods.txt not found!",
        "game_not_found": "Game not found! Exiting...",
        "starting_game": "Starting game...",
        "game_start_failed": "Failed to start the game: {}",
        "fetching_updates": "Fetching updates...",
        "update_completed": "Update process completed!",
        "installing_git": "Installing Git...",
        "installation_completed": "Installation completed!",
        "mod_already_updated": "{} is already up-to-date.",
        "downloading": "Downloading {}...",
        "download_failed": "Failed to download {}!",
        "extracting": "{} successfully downloaded. Extracting...",
        "installed_successfully": "{} installed successfully!",
        "mod_install_complete": "Mod installation process completed!",
        "menu": """
        =======================================
              FurkisPack Management Tool
        =======================================
        1. Start Game
        2. Install & Update FurkisPack
        3. Exit
        =======================================
        """,
        "enter_choice": "Enter your choice [1-3]: ",
        "invalid_choice": "Invalid choice! Please try again.",
        "press_enter": "Press enter to continue"
    },
    "nl": {
        "git_installation_complete": "Git-installatie voltooid!",
        "git_folder_not_found": ".git-map niet gevonden. Repository initialiseren...",
        "cleaning_files": "Onnodige bestanden opruimen...",
        "game_directory_not_found": "Lethal Company-map niet gevonden. Afsluiten...",
        "download_progress": "Downloadvoortgang: {:.2f}%",
        "download_complete": "Download voltooid!",
        "mods_file_not_found": "external_mods.txt niet gevonden!",
        "game_not_found": "Spel niet gevonden! Afsluiten...",
        "starting_game": "Spel starten...",
        "game_start_failed": "Kan het spel niet starten: {}",
        "fetching_updates": "Updates ophalen...",
        "update_completed": "Updateproces voltooid!",
        "installing_git": "Git installeren...",
        "installation_completed": "Installatie voltooid!",
        "mod_already_updated": "{} is al up-to-date.",
        "downloading": "{} wordt gedownload...",
        "download_failed": "Downloaden van {} mislukt!",
        "extracting": "{} succesvol gedownload. Uitpakken...",
        "installed_successfully": "{} succesvol geïnstalleerd!",
        "mod_install_complete": "Mod-installatieproces voltooid!",
        "menu": """
        =======================================
            FurkisPack Beheerhulpmiddel
        =======================================
        1. Spel starten
        2. FurkisPack installeren & bijwerken
        3. Afsluiten
        =======================================
        """,
        "enter_choice": "Voer uw keuze in [1-3]: ",
        "invalid_choice": "Ongeldige keuze! Probeer het opnieuw.",
        "press_enter": "Druk op enter om door te gaan"
    }
}



def get_system_language():
    lang, encoding = locale.getlocale()
    if lang.startswith("Turkish"): lang = "tr"
    elif lang.startswith("Dutch"): lang = "nl"
    else: lang = "en"
    return lang

LANG = get_system_language()
MSG = MESSAGES[LANG]


def download_file(url, dest_path):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    downloaded_size = 0
    
    if response.status_code == 200:
        with open(dest_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=65536):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    if total_size > 0:
                        percent_complete = (downloaded_size / total_size) * 100
                        print(f"\r{MSG['download_progress'].format(percent_complete)}", end="", flush=True)
        print(f"\n{MSG['download_complete']}")
        return True
    return False

def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def read_installed_mods(installed_mods_path):
    installed_mods = {}
    if os.path.exists(installed_mods_path):
        with open(installed_mods_path, "r") as f:
            for line in f:
                parts = line.strip().split("=")
                if len(parts) == 2:
                    installed_mods[parts[0]] = parts[1]
    return installed_mods

def write_installed_mods(installed_mods_path, installed_mods):
    with open(installed_mods_path, "w") as f:
        for mod_name, version in installed_mods.items():
            f.write(f"{mod_name}={version}\n")

def install_external_mods(game_dir):
    mods_file = os.path.join(game_dir, "external_mods.txt")
    installed_mods_file = os.path.join(game_dir, "installed_mods.txt")
    plugins_dir = os.path.join(game_dir, "BepInEx", "plugins", "externals")
    
    if not os.path.exists(plugins_dir):
        os.makedirs(plugins_dir)
    
    if not os.path.exists(mods_file):
        print(MSG["mods_file_not_found"])
        return
    
    installed_mods = read_installed_mods(installed_mods_file)
    
    with open(mods_file, "r") as f:
        for line in f:
            parts = line.strip().split(";")
            if len(parts) != 3:
                continue
            
            mod_name, version, url = parts
            mod_path = os.path.join(plugins_dir, mod_name)
            
            if mod_name in installed_mods and installed_mods[mod_name] == version:
                print(MSG["mod_already_updated"].format(mod_name))
                continue
            
            print(MSG["downloading"].format(mod_name))
            zip_path = os.path.join(game_dir, f"{mod_name}.zip")
            if download_file(url, zip_path):
                print(MSG["extracting"].format(mod_name))
                
                if os.path.exists(mod_path):
                    shutil.rmtree(mod_path)
                os.makedirs(mod_path)
                
                extract_zip(zip_path, mod_path)
                os.remove(zip_path)
                installed_mods[mod_name] = version
                print(MSG["installed_successfully"].format(mod_name))
            else:
                print(MSG["download_failed"].format(mod_name))
    
    write_installed_mods(installed_mods_file, installed_mods)
    print(MSG["mod_install_complete"])


def find_game_directory(is_exe_path = False, search_value = "Lethal Company"):
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

def check_git():
    try:
        subprocess.run(["git", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def install_git():
    if not check_git():
        print(MSG["installing_git"])
        subprocess.run(["winget", "install", "--id", "Git.Git", "-e", "--source", "winget"], shell=True)
    print(MSG["git_installation_complete"])

def fetch_origin_and_reset_local_repo(game_dir, repo_url=REPOSITORY_URL):
    os.chdir(game_dir)
    
    if not os.path.exists(os.path.join(game_dir, ".git")):
        print(MSG["git_folder_not_found"])
        subprocess.run(["git", "init"], shell=True)
        subprocess.run(["git", "remote", "add", "origin", repo_url], shell=True)
    
    print(MSG["fetching_updates"])
    subprocess.run(["git", "fetch", "origin", "main", "no-mod", "--depth=1"], shell=True) 
    subprocess.run(["git", "reset", "--hard", "origin/main"], shell=True)

    
    print(MSG["cleaning_files"])
    
    subprocess.run(["git", "clean", "-fd"], shell=True)
    
    print(MSG["update_completed"])



def install_and_update():
    game_dir = find_game_directory()
    if not game_dir:
        print(MSG["game_directory_not_found"])
        return
    install_git()
    fetch_origin_and_reset_local_repo(game_dir=game_dir)
    install_external_mods(game_dir=game_dir)


def start_game():
    game_exe_path = find_game_directory(is_exe_path=True)
    if not game_exe_path:
        print(MSG["game_not_found"])
        return
    try:
        print(MSG["starting_game"])
        subprocess.Popen(game_exe_path, shell=True)
    except Exception as e:
        print(MSG["game_start_failed"].format(e))



def main():
    while True:
        print(MSG["menu"])
        choice = input(MSG["enter_choice"])
        
        if choice == "1":
            start_game()
        elif choice == "2":
            install_and_update()
        elif choice == "3":
            break
        else:
            print(MSG["invalid_choice"])
        input(MSG["press_enter"])
        

if __name__ == "__main__":
    main()
