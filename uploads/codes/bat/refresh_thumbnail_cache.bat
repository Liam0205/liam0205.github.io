@echo off
taskkill /f /im explorer.exe
cd /d %userprofile%\AppData\Local
del IconCache.db /a
start explorer.exe
echo done.
