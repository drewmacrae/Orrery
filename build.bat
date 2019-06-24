set PATH=%PATH%;C:\Windows\System32\downlevel;
py -m PyInstaller orrery.py
copy *.ogg dist\orrery
copy *.ttf dist\orrery
