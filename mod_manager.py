import os
import requests
import zipfile
import shutil
import subprocess
import locale
import winreg


import locale

def get_system_language():
    lang, encoding = locale.getlocale()
    if lang.startswith("Turkish") or lang.startswith("Türkçe"): lang = "tr"
    else: lang = "en"
    return lang


MESSAGES = {
    "tr": {
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
    }
}
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
                        print(f"\rİndirme ilerlemesi: {percent_complete:.2f}%", end="", flush=True)
        print("\nİndirme tamamlandı!")
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
        print("external_mods.txt bulunamadı!")
        return
    
    installed_mods = read_installed_mods(installed_mods_file)
    
    with open(mods_file, "r") as f:
        for line in f:
            parts = line.strip().split(";")
            if len(parts) != 3:
                
                print(parts)
                continue
            
            mod_name, version, url = parts
            mod_path = os.path.join(plugins_dir, mod_name)
            
            if mod_name in installed_mods and installed_mods[mod_name] == version:
                print(f"{mod_name} zaten güncel.")
                continue
            
            print(f"{mod_name} indiriliyor...")
            zip_path = os.path.join(game_dir, f"{mod_name}.zip")
            if download_file(url, zip_path):
                print(f"{mod_name} başarıyla indirildi. Çıkarılıyor...")
                
                if os.path.exists(mod_path):
                    shutil.rmtree(mod_path)
                os.makedirs(mod_path)
                
                extract_zip(zip_path, mod_path)
                os.remove(zip_path)
                installed_mods[mod_name] = version
                print(f"{mod_name} başarıyla yüklendi!")
            else:
                print(f"{mod_name} indirilemedi!")
    
    write_installed_mods(installed_mods_file, installed_mods)
    print("Mod yükleme işlemi tamamlandı!")


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
        print("Installing Git...")
        subprocess.run(["winget", "install", "--id", "Git.Git", "-e", "--source", "winget"], shell=True)
    print("Installation completed!")

def fetch_origin_and_reset_local_repo(game_dir, repo_url="https://github.com/furkanaliunal/lethal_company_mod_pack.git"):
    os.chdir(game_dir)
    
    if not os.path.exists(os.path.join(game_dir, ".git")):
        print(".git folder not found. Initializing repository...")
        subprocess.run(["git", "init"], shell=True)
        subprocess.run(["git", "remote", "add", "origin", repo_url], shell=True)
    
    print("Fetching updates...")
    subprocess.run(["git", "fetch", "origin", "main", "no-mod", "--depth=1"], shell=True) 
    subprocess.run(["git", "reset", "--hard", "origin/main"], shell=True)

    
    print("Cleaning up unnecessary files...")
    
    subprocess.run(["git", "clean", "-fd"], shell=True)
    
    print("Update process completed!")



def install_and_update():
    game_dir = find_game_directory()
    if not game_dir:
        print("Failed to locate Lethal Company directory. Exiting...")
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
