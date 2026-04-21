# Shot Loader for Nuke
#
# Expected folder structure:
#     Root_Directory/
#         Project_A/
#             Sequence_001/
#                 Shot_001/
#                     Element_001/
#                         Project_A_Sequence_001_Shot_001_Element_001_v0001.nk
#                         Project_A_Sequence_001_Shot_001_Element_001_v0002.nk
#                     Element_002/
#                 Shot_002/
#             Sequence_002/
#         Project_B/

import os

from PySide2 import QtCore, QtWidgets
from PySide2.QtWidgets import QFileDialog

import nuke


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        self.dialog = Dialog  # Store reference so saveScene can close it safely

        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 258)

        self.label_root_directory = QtWidgets.QLabel(Dialog)
        self.label_root_directory.setGeometry(QtCore.QRect(20, 0, 191, 20))
        self.label_root_directory.setObjectName("label_root_directory")
        self.label_root_directory.setText("Select your root directory")

        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(20, 20, 191, 20))
        self.lineEdit.setObjectName("lineEdit")

        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(220, 20, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.browsefiles)

        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(300, 220, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(Dialog.close)

        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(300, 20, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.loadfiles)

        self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        self.pushButton_4.setGeometry(QtCore.QRect(220, 220, 75, 23))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.loadScene)

        self.pushButton_5 = QtWidgets.QPushButton(Dialog)
        self.pushButton_5.setGeometry(QtCore.QRect(140, 220, 75, 23))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.saveScene)

        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(130, 60, 100, 22))
        self.comboBox.setObjectName("comboBox")

        self.comboBox_2 = QtWidgets.QComboBox(Dialog)
        self.comboBox_2.setGeometry(QtCore.QRect(130, 90, 100, 22))
        self.comboBox_2.setObjectName("comboBox_2")

        self.comboBox_3 = QtWidgets.QComboBox(Dialog)
        self.comboBox_3.setGeometry(QtCore.QRect(130, 120, 100, 22))
        self.comboBox_3.setObjectName("comboBox_3")

        self.comboBox_4 = QtWidgets.QComboBox(Dialog)
        self.comboBox_4.setGeometry(QtCore.QRect(130, 150, 100, 22))
        self.comboBox_4.setObjectName("comboBox_4")

        self.comboBox_5 = QtWidgets.QComboBox(Dialog)
        self.comboBox_5.setGeometry(QtCore.QRect(130, 180, 100, 22))
        self.comboBox_5.setObjectName("comboBox_5")

        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(50, 60, 49, 141))
        self.widget.setObjectName("widget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.verticalLayout.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.verticalLayout.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.verticalLayout.addWidget(self.label_5)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.comboBox.currentIndexChanged.connect(self.update_sequence)
        self.comboBox_2.currentIndexChanged.connect(self.update_shot)
        self.comboBox_3.currentIndexChanged.connect(self.update_element)
        self.comboBox_4.currentIndexChanged.connect(self.update_version)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Shot Loader"))
        self.pushButton.setText(_translate("Dialog", "Browse"))
        self.pushButton_2.setText(_translate("Dialog", "Cancel"))
        self.pushButton_3.setText(_translate("Dialog", "Load"))
        self.pushButton_4.setText(_translate("Dialog", "Open Scene"))
        self.pushButton_5.setText(_translate("Dialog", "Save Scene"))
        self.label.setText(_translate("Dialog", "Project"))
        self.label_2.setText(_translate("Dialog", "Sequence"))
        self.label_3.setText(_translate("Dialog", "Shot"))
        self.label_4.setText(_translate("Dialog", "Element"))
        self.label_5.setText(_translate("Dialog", "Version"))

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _root(self):
        """Single source of truth for the root directory."""
        return self.lineEdit.text().strip()

    def _list_subfolders(self, path):
        """Return sorted subfolder names in path, or [] on any OS error."""
        try:
            return sorted(
                f for f in os.listdir(path)
                if os.path.isdir(os.path.join(path, f))
            )
        except OSError as e:
            print(f"[Shot Loader] Could not read {path}: {e}")
            return []

    # ------------------------------------------------------------------
    # UI callbacks
    # ------------------------------------------------------------------

    def browsefiles(self):
        # Start at user's home directory — portable across machines
        start_dir = self._root() or os.path.expanduser("~")
        folder_path = QFileDialog.getExistingDirectory(None, "Select Folder", start_dir)
        if folder_path:
            self.lineEdit.setText(folder_path)

    def loadfiles(self):
        # Clear everything downstream before repopulating
        self.comboBox.clear()
        self.comboBox_2.clear()
        self.comboBox_3.clear()
        self.comboBox_4.clear()
        self.comboBox_5.clear()

        root = self._root()
        if not root or not os.path.isdir(root):
            QtWidgets.QMessageBox.warning(
                None, "Error", "No valid root folder selected. Please Browse first."
            )
            return

        projects = self._list_subfolders(root)
        if not projects:
            QtWidgets.QMessageBox.information(
                None, "No Projects", "No project folders found in the selected root."
            )
            return

        self.comboBox.addItems(projects)
        # Explicitly trigger the cascade in case the signal didn't fire
        self.update_sequence()

    def update_sequence(self):
        self.comboBox_2.clear()
        self.comboBox_3.clear()
        self.comboBox_4.clear()
        self.comboBox_5.clear()

        project_folder = self.comboBox.currentText()
        if not project_folder:
            return

        project_path = os.path.join(self._root(), project_folder)
        sequences = self._list_subfolders(project_path)
        if sequences:
            self.comboBox_2.addItems(sequences)

    def update_shot(self):
        self.comboBox_3.clear()
        self.comboBox_4.clear()
        self.comboBox_5.clear()

        sequence_folder = self.comboBox_2.currentText()
        if not sequence_folder:
            return

        sequence_path = os.path.join(
            self._root(), self.comboBox.currentText(), sequence_folder
        )
        shots = self._list_subfolders(sequence_path)
        if shots:
            self.comboBox_3.addItems(shots)

    def update_element(self):
        self.comboBox_4.clear()
        self.comboBox_5.clear()

        shot_folder = self.comboBox_3.currentText()
        if not shot_folder:
            return

        shot_path = os.path.join(
            self._root(),
            self.comboBox.currentText(),
            self.comboBox_2.currentText(),
            shot_folder,
        )
        elements = self._list_subfolders(shot_path)
        if elements:
            self.comboBox_4.addItems(elements)

    def update_version(self):
        self.comboBox_5.clear()

        element_folder = self.comboBox_4.currentText()
        if not element_folder:
            return

        element_path = os.path.join(
            self._root(),
            self.comboBox.currentText(),
            self.comboBox_2.currentText(),
            self.comboBox_3.currentText(),
            element_folder,
        )
        if not os.path.isdir(element_path):
            return

        # Collect .nk files only, strip extension, extract trailing vXXXX token
        version_tokens = []
        try:
            for f in os.listdir(element_path):
                full = os.path.join(element_path, f)
                if not os.path.isfile(full) or not f.lower().endswith(".nk"):
                    continue
                stem = os.path.splitext(f)[0]
                token = stem.split("_")[-1]
                if token.startswith("v") and token[1:].isdigit():
                    version_tokens.append(token)
        except OSError as e:
            print(f"[Shot Loader] Could not read {element_path}: {e}")
            return

        # Sort numerically, latest first
        version_tokens.sort(key=lambda v: int(v[1:]), reverse=True)
        self.comboBox_5.addItems(version_tokens)

    # ------------------------------------------------------------------
    # Scene actions
    # ------------------------------------------------------------------

    def loadScene(self):
        project_name = self.comboBox.currentText()
        sequence_name = self.comboBox_2.currentText()
        shot_name = self.comboBox_3.currentText()
        element_name = self.comboBox_4.currentText()
        version_name = self.comboBox_5.currentText()

        if not all([project_name, sequence_name, shot_name, element_name, version_name]):
            QtWidgets.QMessageBox.warning(
                None, "Error", "Please select a project, sequence, shot, element, and version."
            )
            return

        file_name = f"{project_name}_{sequence_name}_{shot_name}_{element_name}_{version_name}.nk"
        full_file_path = os.path.normpath(
            os.path.join(
                self._root(), project_name, sequence_name, shot_name, element_name, file_name
            )
        )

        if os.path.isfile(full_file_path):
            nuke.scriptOpen(full_file_path)
            QtWidgets.QMessageBox.information(
                None, "Scene Opened", f"Opened:\n{full_file_path}"
            )
        else:
            QtWidgets.QMessageBox.warning(
                None, "File Not Found", f"Could not find:\n{full_file_path}"
            )

    def saveScene(self):
        root_directory = self._root()
        if not root_directory:
            QtWidgets.QMessageBox.warning(None, "Error", "Root directory not selected.")
            return

        project_name = self.comboBox.currentText()
        sequence_name = self.comboBox_2.currentText()
        shot_name = self.comboBox_3.currentText()
        element_name = self.comboBox_4.currentText()

        if not all([project_name, sequence_name, shot_name, element_name]):
            QtWidgets.QMessageBox.warning(
                None, "Error", "Please select a project, sequence, shot, and element."
            )
            return

        expected_folder_path = os.path.join(
            root_directory, project_name, sequence_name, shot_name, element_name
        )
        if not os.path.isdir(expected_folder_path):
            QtWidgets.QMessageBox.warning(
                None, "Error", f"Target save directory does not exist:\n{expected_folder_path}"
            )
            return

        # Find existing versions in the folder
        prefix = f"{project_name}_{sequence_name}_{shot_name}_{element_name}_"
        version_numbers = []
        try:
            for f in os.listdir(expected_folder_path):
                if not (f.startswith(prefix) and f.lower().endswith(".nk")):
                    continue
                token = os.path.splitext(f)[0].split("_")[-1]
                if token.startswith("v") and token[1:].isdigit():
                    version_numbers.append(int(token[1:]))
        except OSError as e:
            QtWidgets.QMessageBox.warning(
                None, "Error", f"Could not scan target directory:\n{e}"
            )
            return

        new_version = max(version_numbers) + 1 if version_numbers else 1
        new_version_str = f"v{new_version:04d}"
        new_file_name = f"{prefix}{new_version_str}.nk"
        new_file_path = os.path.normpath(os.path.join(expected_folder_path, new_file_name))

        try:
            nuke.scriptSaveAs(new_file_path)
        except RuntimeError as e:
            QtWidgets.QMessageBox.warning(None, "Save Failed", f"Nuke could not save:\n{e}")
            return

        QtWidgets.QMessageBox.information(
            None, "Save Successful", f"Scene saved as:\n{new_file_path}"
        )
        self.dialog.close()


def show_dialog():
    """Open the Shot Loader dialog. Called from the Nuke menu."""
    # Reuse the existing QApplication that Nuke already owns
    dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(dialog)
    dialog.exec_()


# Register the menu entry — the dialog only opens when the user clicks the menu item
nuke.menu("Nuke").addCommand("Tools/Shot Loader", show_dialog)
