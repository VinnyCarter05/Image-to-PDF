### use CMD line python setup.py build

from cx_Freeze import setup, Executable

base = None    

executables = [Executable(
    "mfmcimg2pdf.py",
    base="Win32GUI",
    icon="mfmclogo.ico",
    targetName="mfmcFaxConvert.exe")]

packages = ["idna", "os", "sys", "PyQt5", "img2PDF", "mainwindow4", "welcome3", "mfmcimg2pdf_rc", ]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "mfmcFaxConvert",
    options = options,
    version = "1.1",
    description = 'Convert img to PDF',
    executables = executables
)
