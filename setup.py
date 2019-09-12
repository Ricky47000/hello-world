import sys, os
from cx_Freeze import setup, Executable

os.environ['TCL_LIBRARY'] = "C:\\Users\\nxf07154\\AppData\\Local\\Programs\\Python\\Python35-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\nxf07154\\AppData\\Local\\Programs\\Python\\Python35-32\\tcl\\tk8.6"

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": []}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = 'Console'
if sys.platform == "win32":
	base = "Win32GUI"

options = {
	'build_exe': {
		'includes': ['tkinter','atexit','PyQt5', 'matplotlib', 'reportlab', 'numpy','numpy.core._methods', 'numpy.lib.format','xml', 'PyQt5.uic', 'mpldatacursor', 'lxml._elementpath'],
		'include_files': ['icon.png','C:\\Users\\nxf07154\\AppData\\Local\\Programs\\Python\\Python35-32\\DLLs\\tcl86t.dll','C:\\Users\\nxf07154\\AppData\\Local\\Programs\\Python\\Python35-32\\DLLs\\tk86t.dll', 'C:\\Users\\nxf07154\\AppData\\Local\\Programs\\Python\\Python35-32\\DLLs\\_tkinter.pyd'],
	
		'excludes': ['gtk', 'PyQt4']
	}
}


setup(  name = "Curve Trace Reporting Tool",
		version = "1.0",
		description = "Additional CT module - Reporting, Limits Calculation, Deviation Classification",
		options = options,
		executables = [Executable("Curve_Trace_Reporting_Tool.py", base=base, icon="icon.ico")])
