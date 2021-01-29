## World of Warcraft Fishing Bot
Frame comparison based fishing bot for World of Warcraft. Success rate ~80%

## Setup
### Create python3 virtual environment 
```
python3 -m venv venv
```

### Activate venv
```
source venv/bin/activate
```

### install dependencies
```
pipenv install
```

### Run bot (you have 2 seconds activate WoW window)
```
python fishing_bot.py
```

## Info

Bot works by comparing two frames. It recognises catch when fishing float changes position and then 
returns to original position. This happens when it dips down

Image capture is at `(x-1400, y-200)` square from left top corner. Check `base_screenshot.png` to see where exactly bot is fishing 

* **Move player camera so fishing floater appears inside image capture square!**
* **Put fishing skill in action bar under button `1`**
* Obviously, don't move camera while fishing


## Troubleshooting

* Bot thinks fish is caught when it's not. Try finding calmer waters. 
  There's too much noise between two frames - difference between frames is what makes 
  bot think there's a catch! 
  
* Bot does not catch fish, after fishing float moves. This is caused because there's not 
  enough change between frames. Another solution - try to make another `lure.png` screenshot
  or change video settings

* Bot does not start (`pyautogui` issue). Mac needs separate OS level permissions: 
  `Preferences > Security & Privacy > Accessibility > iTerm`