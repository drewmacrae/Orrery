set PATH=%PATH%;C:\Windows\System32\downlevel;
py -m PyInstaller Connector.py
copy *.ogg dist\Connector
copy *.ttf dist\Connector
