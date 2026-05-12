import nuke
import os


def show_dialog():
    try:
        from PySide2 import QtCore, QtWidgets
    except ImportError:
        from PySide6 import QtCore, QtWidgets
    try:
        from PySide2.QtWidgets import QFileDialog
    except ImportError:
        from PySide6.QtWidgets import QFileDialog

    class ShotLoaderDialog(QtWidgets.QDialog):
        def __init__(self):
            super(ShotLoaderDialog, self).__init__()
            self.setWindowTitle("Shot Loader")
            self.resize(400, 258)

            self.label_root = QtWidgets.QLabel("Select your root directory", self)
            self.label_root.setGeometry(QtCore.QRect(20, 0, 191, 20))

            self.lineEdit = QtWidgets.QLineEdit(self)
            self.lineEdit.setGeometry(QtCore.QRect(20, 20, 191, 20))

            btn_browse = QtWidgets.QPushButton("Browse", self)
            btn_browse.setGeometry(QtCore.QRect(220, 20, 75, 23))
            btn_browse.clicked.connect(self.browsefiles)

            btn_load = QtWidgets.QPushButton("Load", self)
            btn_load.setGeometry(QtCore.QRect(300, 20, 75, 23))
            btn_load.clicked.connect(self.loadfiles)

            btn_cancel = QtWidgets.QPushButton("Cancel", self)
            btn_cancel.setGeometry(QtCore.QRect(300, 220, 75, 23))
            btn_cancel.clicked.connect(self.close)

            btn_open_scene = QtWidgets.QPushButton("Open Scene", self)
            btn_open_scene.setGeometry(QtCore.QRect(220, 220, 75, 23))
            btn_open_scene.clicked.connect(self.loadScene)

            btn_save_scene = QtWidgets.QPushButton("Save Scene", self)
            btn_save_scene.setGeometry(QtCore.QRect(140, 220, 75, 23))
            btn_save_scene.clicked.connect(self.saveScene)

            self.comboBox   = QtWidgets.QComboBox(self)
            self.comboBox.setGeometry(QtCore.QRect(130, 60, 100, 22))
            self.comboBox_2 = QtWidgets.QComboBox(self)
            self.comboBox_2.setGeometry(QtCore.QRect(130, 90, 100, 22))
            self.comboBox_3 = QtWidgets.QComboBox(self)
            self.comboBox_3.setGeometry(QtCore.QRect(130, 120, 100, 22))
            self.comboBox_4 = QtWidgets.QComboBox(self)
            self.comboBox_4.setGeometry(QtCore.QRect(130, 150, 100, 22))
            self.comboBox_5 = QtWidgets.QComboBox(self)
            self.comboBox_5.setGeometry(QtCore.QRect(130, 180, 100, 22))

            widget = QtWidgets.QWidget(self)
            widget.setGeometry(QtCore.QRect(50, 60, 49, 141))
            vbox = QtWidgets.QVBoxLayout(widget)
            vbox.setContentsMargins(0, 0, 0, 0)
            for lbl in ["Project", "Sequence", "Shot", "Element", "Version"]:
                vbox.addWidget(QtWidgets.QLabel(lbl))

            self.comboBox.currentIndexChanged.connect(self.update_sequence)
            self.comboBox_2.currentIndexChanged.connect(self.update_shot)
            self.comboBox_3.currentIndexChanged.connect(self.update_element)
            self.comboBox_4.currentIndexChanged.connect(self.update_version)

        def _root(self):
            return self.lineEdit.text().strip()

        def _list_subfolders(self, path):
            try:
                return sorted(f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f)))
            except OSError as e:
                print("[Shot Loader] Could not read {}: {}".format(path, e))
                return []

        def browsefiles(self):
            start_dir = self._root() or os.path.expanduser("~")
            folder_path = QFileDialog.getExistingDirectory(None, "Select Folder", start_dir)
            if folder_path:
                self.lineEdit.setText(folder_path)

        def loadfiles(self):
            self.comboBox.clear()
            self.comboBox_2.clear()
            self.comboBox_3.clear()
            self.comboBox_4.clear()
            self.comboBox_5.clear()
            root = self._root()
            if not root or not os.path.isdir(root):
                QtWidgets.QMessageBox.warning(None, "Error", "No valid root folder selected. Please Browse first.")
                return
            projects = self._list_subfolders(root)
            if not projects:
                QtWidgets.QMessageBox.information(None, "No Projects", "No project folders found in the selected root.")
                return
            self.comboBox.addItems(projects)
            self.update_sequence()

        def update_sequence(self):
            self.comboBox_2.clear()
            self.comboBox_3.clear()
            self.comboBox_4.clear()
            self.comboBox_5.clear()
            project = self.comboBox.currentText()
            if project:
                self.comboBox_2.addItems(self._list_subfolders(os.path.join(self._root(), project)))

        def update_shot(self):
            self.comboBox_3.clear()
            self.comboBox_4.clear()
            self.comboBox_5.clear()
            seq = self.comboBox_2.currentText()
            if seq:
                path = os.path.join(self._root(), self.comboBox.currentText(), seq)
                self.comboBox_3.addItems(self._list_subfolders(path))

        def update_element(self):
            self.comboBox_4.clear()
            self.comboBox_5.clear()
            shot = self.comboBox_3.currentText()
            if shot:
                path = os.path.join(self._root(), self.comboBox.currentText(), self.comboBox_2.currentText(), shot)
                self.comboBox_4.addItems(self._list_subfolders(path))

        def update_version(self):
            self.comboBox_5.clear()
            element = self.comboBox_4.currentText()
            if not element:
                return
            element_path = os.path.join(
                self._root(), self.comboBox.currentText(),
                self.comboBox_2.currentText(), self.comboBox_3.currentText(), element
            )
            if not os.path.isdir(element_path):
                return
            version_tokens = []
            try:
                for f in os.listdir(element_path):
                    if os.path.isfile(os.path.join(element_path, f)) and f.lower().endswith(".nk"):
                        token = os.path.splitext(f)[0].split("_")[-1]
                        if token.startswith("v") and token[1:].isdigit():
                            version_tokens.append(token)
            except OSError as e:
                print("[Shot Loader] Could not read {}: {}".format(element_path, e))
                return
            version_tokens.sort(key=lambda v: int(v[1:]), reverse=True)
            self.comboBox_5.addItems(version_tokens)

        def loadScene(self):
            vals = [self.comboBox.currentText(), self.comboBox_2.currentText(),
                    self.comboBox_3.currentText(), self.comboBox_4.currentText(),
                    self.comboBox_5.currentText()]
            if not all(vals):
                QtWidgets.QMessageBox.warning(None, "Error", "Please select a project, sequence, shot, element, and version.")
                return
            project, seq, shot, element, version = vals
            file_name = "{}_{}_{}_{}_{}.nk".format(project, seq, shot, element, version)
            full_path = os.path.normpath(os.path.join(self._root(), project, seq, shot, element, file_name))
            if os.path.isfile(full_path):
                nuke.scriptOpen(full_path)
                QtWidgets.QMessageBox.information(None, "Scene Opened", "Opened:\n{}".format(full_path))
            else:
                QtWidgets.QMessageBox.warning(None, "File Not Found", "Could not find:\n{}".format(full_path))

        def saveScene(self):
            root = self._root()
            if not root:
                QtWidgets.QMessageBox.warning(None, "Error", "Root directory not selected.")
                return
            project = self.comboBox.currentText()
            seq     = self.comboBox_2.currentText()
            shot    = self.comboBox_3.currentText()
            element = self.comboBox_4.currentText()
            if not all([project, seq, shot, element]):
                QtWidgets.QMessageBox.warning(None, "Error", "Please select a project, sequence, shot, and element.")
                return
            folder = os.path.join(root, project, seq, shot, element)
            if not os.path.isdir(folder):
                QtWidgets.QMessageBox.warning(None, "Error", "Target save directory does not exist:\n{}".format(folder))
                return
            prefix = "{}_{}_{}_{}_".format(project, seq, shot, element)
            version_numbers = []
            try:
                for f in os.listdir(folder):
                    if f.startswith(prefix) and f.lower().endswith(".nk"):
                        token = os.path.splitext(f)[0].split("_")[-1]
                        if token.startswith("v") and token[1:].isdigit():
                            version_numbers.append(int(token[1:]))
            except OSError as e:
                QtWidgets.QMessageBox.warning(None, "Error", "Could not scan target directory:\n{}".format(e))
                return
            new_version = max(version_numbers) + 1 if version_numbers else 1
            new_file = "{}{}.nk".format(prefix, "v{:04d}".format(new_version))
            new_path = os.path.normpath(os.path.join(folder, new_file))
            try:
                nuke.scriptSaveAs(new_path)
            except RuntimeError as e:
                QtWidgets.QMessageBox.warning(None, "Save Failed", "Nuke could not save:\n{}".format(e))
                return
            QtWidgets.QMessageBox.information(None, "Save Successful", "Scene saved as:\n{}".format(new_path))
            self.close()

    dialog = ShotLoaderDialog()
    dialog.exec_()


nuke.menu('Nuke').addCommand('NDToolKit/Shot Loader', show_dialog)
