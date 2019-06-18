# Wox.Plugin.SteamGames
A steam game launcher plugin for Wox

When you first time using this function, type `/st` and wait a second for setting up.

![preview](https://github.com/mycraftmw/Wox.Plugin.SteamGames/blob/master/preview.png)

# Requirements
This plugin requries the python module `requests` and `bs4`.
To install these, open a command prompt and run these two commands:

`pip install requests`

`pip install bs4`

# Configuration

Edit the config.json in the wox plugin settings folder and put your steam library folder(s) inside.

Examples:

Single Steam Library:
```
{
    "steamapps_dir": "C:\\Games\\steamapps"
}
```

Multiple Steam Libraries:
```
{
    "steamapps_dir": ["C:\\Games\\steamapps", "D:\\Games\\Steam\\steamapps"]
}
```
