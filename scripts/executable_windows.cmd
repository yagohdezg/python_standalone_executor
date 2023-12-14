pushd %~dp0
call .\venv\Scripts\activate.bat
setlocal
cd ..

set NAME=DESCARGAR_ABOGADOS
@REM python .\scripts\pyinstaller_command.py %NAME%
pyinstaller --onefile -n %NAME% .\src\wrapper.py --paths=.\venv\Lib\site-packages --hidden-import tkinter --hidden-import tkinter.ttk

del %NAME%.spec
echo y | rmdir /s build
move .\dist\%NAME%.exe .\tests\%NAME%.exe
echo y | rmdir /s dist
xcopy .\src .\tests\src /e /i /Y
copy .\app_conf.yaml .\tests\app_conf.yaml
@REM .\tests\%NAME%.exe
endlocal

popd