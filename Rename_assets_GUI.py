import unreal
import sys

sys.path.append(r"C:\Users\Carlos David\AppData\Local\Programs\Python\Python39\Lib\site-packages")

from PySide2 import QtCore, QtGui, QtUiTools
from PySide2.QtWidgets import QWidget, QApplication, QLineEdit, QCheckBox, QPushButton

def rename_assets(search_pattern, replace_pattern, use_case):
    # instancias da unreal classes
    system_lib = unreal.SystemLibrary()
    editor_util = unreal.EditorUtilityLibrary()
    string_lib = unreal.StringLibrary()

    #selecionando os assets
    selected_assets = editor_util.get_selected_assets()
    num_assets = len(selected_assets)
    replaced = 0

    unreal.log(f"Selected {num_assets} asset/s")

    #loop para pegar os nomes dos assets e renomealos
    for asset in selected_assets:
        asset_name = system_lib.get_object_name(asset)#pegando nome

        #checando se o asset name tem o renome que deram
        if string_lib.contains(asset_name, search_pattern, use_case=use_case):
            search_case = unreal.SearchCase.CASE_SENSITIVE if use_case else unreal.SearchCase.IGNORE_CASE
            replaced_name = string_lib.replace(asset_name, search_pattern, replace_pattern, search_case=search_case)
            editor_util.rename_asset(asset, replaced_name)

            replaced += 1
            unreal.log(f"Replaced {asset_name} with {replaced_name}")
        else:
            unreal.log(f"{asset_name} did not match the search pattern, was skipped")

    unreal.log(f"Replaced {replaced} of {num_assets} assets")

class RenameGUI(QWidget):
    def __init__(self, parent=None):
        super(RenameGUI, self).__init__(parent)

        #carregando o GUI criado
        self.widget = QtUiTools.QUiLoader().load(r'C:\Users\Carlos David\AppData\Local\Programs\Python\Python39\Lib\site-packages\qt5_applications\Qt\bin\Rename.ui')
        self.widget.setParent(self)

        self.widget.setGeometry(0, 0, self.widget.width(), self.widget.height())

        #fazendo as interações com os elementos
        self.search = self.widget.findChild(QLineEdit, "searchPattern")
        self.replace = self.widget.findChild(QLineEdit, "replacePattern")

        self.use_case = self.widget.findChild(QCheckBox, "checkBox")

        #trigger do pushbutton
        self.rename_button = self.widget.findChild(QPushButton, "pushButton")
        self.rename_button.clicked.connect(self.rename_handler)

    def rename_handler(self):
        search_pattern = self.search.text()
        replace_pattern = self.replace.text()
        use_case = self.use_case.isChecked()

        rename_assets(search_pattern, replace_pattern, use_case)

app = None
if not QApplication.instance():
    app = QApplication(sys.argv)

#Start GUI
window = RenameGUI()
window.show()