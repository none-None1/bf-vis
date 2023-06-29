pyi-makespec main_pack.py -w -i icon.ico -F -n "brainfuck-visualizer" --add-binary pointer.png;. --add-binary icon.png;.  --disable-windowed-traceback
pyinstaller brainfuck-visualizer.spec

