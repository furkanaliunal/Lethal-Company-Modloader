<div align="center">

![](logo.ico "Icon")

</div>
<br>

# Lethal Company Modloader


## 📄 **Description**

This repository is designed to provide a practical and centralized solution for managing and installing mods for the game **Lethal Company**. Use it as a starting point or as a reference to build your own modding framework.

Feel free to customize, enhance, and expand it as you see fit. Contributions and improvements are always welcome!


## 🎉 **Benefits**

This repository provides significant benefits by offering a centralized system for modding Lethal Company, making it easier to develop and distribute mods. With a centralized approach, all team members can quickly access and integrate the latest mod updates and packages, ensuring everyone is on the same page and using the most up-to-date version. This eliminates the need for individual setups and reduces inconsistencies across different installations. It simplifies collaboration, as all contributors can easily add, modify, or test new mods without worrying about complex setup procedures per player. As a result, the repository helps streamline the modding process for the entire team, promoting efficiency and consistency in managing mods.



## 🎮 **How To Use**

Just download the runnable file (.exe) and double click on it to run. Once the application is started, continue with pressing *update* option. Once installation is done, you are ready to play the game! 


## 🪄 **Required Tools To Develop**

If you want to modify this repository all you need is having Python and Pip installation on your system. If both are ready to use open a command line interface and locate to repository folder. Then execute this pip command

```
pip install -r requirements.txt
```

## 🔨 **How To Build Application**

I prepared a basic build script for Windows operating system users. Double click on "build.bat" file to build your mod_manager.py application. Main benefit of building the application is making it executable without development tools. So your friend can execute it easily.

Here is detailed explanation of building your application using [pyinstaller](https://pyinstaller.org/en/stable/usage.html)


## 🎨 **How To Use For Your Own Modpack**

Check the "region CONFIG" section in the mod_manager.py script. Here, you'll find the REPOSITORY_URL line. Simply replace the value with your repository URL.

Since we're using GitHub to host our mod pack, we need to be mindful of the repository's size limitations. GitHub is best suited for configuration files and smaller mods. For larger files, generate a direct download link and include it in the external_mods.txt file, as shown in the example below:

```
suits_moresuits;1.0.0;https://www.dropbox.com/scl/fi/4ijwxa3wk8iu/moresuits.zip?rlkey=utli561j&st=45usrk5g&dl=1
```

In the example above, each external line consists of three values separated by a semicolon (;):

- Plugin name
- Version
- Download link

Once a mod is downloaded, the script records the version. If a newer version is available in the repository, the script will automatically update the external plugin.


<h3 align="center">


[🎯 Here is the default modpack created by me 🎯](https://github.com/furkanaliunal/Lethal-Company-Modpack)

[📝 Here is an example about external plugin configuration 📝](https://github.com/furkanaliunal/Lethal-Company-Modpack/blob/main/external_mods.txt)


</h3>