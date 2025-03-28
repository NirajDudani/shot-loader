from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QFileDialog
import os
import sys
import nuke


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 258)

        self.label_root_directory = QtWidgets.QLabel(Dialog)
        self.label_root_directory.setGeometry(QtCore.QRect(20, 0, 191, 20))
        self.label_root_directory.setObjectName("label_root_directory")
    
        # Set the text for the label
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
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setObjectName("label_5")
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

    def browsefiles(self):
        folder_path = QFileDialog.getExistingDirectory(None, 'Select Folder', r'D:\Projects\Nuke TD\Shot-Loader')
        if folder_path:
            self.lineEdit.setText(folder_path)
            self.selected_folder = folder_path
    
    def loadfiles(self):
        # Clear comboboxes
        self.comboBox.clear()
        self.comboBox_2.clear()
        self.comboBox_3.clear()
        self.comboBox_4.clear()
        self.comboBox_5.clear()
    
        # Ensure the selected folder is set
        if not hasattr(self, 'selected_folder') or not self.selected_folder:
            QtWidgets.QMessageBox.warning(None, "Error", "No folder selected. Please select a folder first.")
            return  # Exit if no folder is selected
        
        folder_loc = self.selected_folder  # Use self.selected_folder here
    
        # Get all subfolders in the directory
        folders = [f for f in os.listdir(folder_loc) if os.path.isdir(os.path.join(folder_loc, f))]
        self.comboBox.addItems(folders)





    def update_sequence(self):
        project_folder = self.comboBox.currentText()  # Get selected project
        project_path = os.path.join(self.lineEdit.text(), project_folder)
    
        if os.path.isdir(project_path):
            sequence_folders = [f for f in os.listdir(project_path) if os.path.isdir(os.path.join(project_path, f))]
    
            if sequence_folders:
                self.comboBox_2.clear()
                self.comboBox_2.addItems(sequence_folders)
            else:
                self.comboBox_2.clear()
                self.comboBox_2.addItem("No sequences available")
                print(f"No sequence folders found in {project_path}")
        else:
            print(f"Project folder '{project_folder}' is invalid or doesn't exist.")


    def update_shot(self):
        sequence_folder = self.comboBox_2.currentText()
        sequence_path = os.path.join(self.lineEdit.text(), self.comboBox.currentText(), sequence_folder)

        if os.path.isdir(sequence_path):
            shot_folders = []
            for f in os.listdir(sequence_path):  
                if os.path.isdir(os.path.join(sequence_path, f)):  
                    shot_folders.append(f)
            self.comboBox_3.clear()
            self.comboBox_3.addItems(shot_folders)

    def update_element(self):
        shot_folder = self.comboBox_3.currentText()
        shot_path = os.path.join(self.lineEdit.text(), self.comboBox.currentText(), self.comboBox_2.currentText(), shot_folder)

        if os.path.isdir(shot_path):
            element_folders = []
            for f in os.listdir(shot_path):
                if os.path.isdir(os.path.join(shot_path,f)):
                    element_folders.append(f)
            self.comboBox_4.clear()
            self.comboBox_4.addItems(element_folders)

    def update_version(self):
        element_folder = self.comboBox_4.currentText()
        element_path = os.path.join(self.lineEdit.text(), self.comboBox.currentText(), self.comboBox_2.currentText(), self.comboBox_3.currentText(), element_folder)

        version_folders = []
        if os.path.isdir(element_path):
            version_folders = []
            
            for f in os.listdir(element_path):
                version_folders.append(f.split('_')[-1])

        self.comboBox_5.clear()
        self.comboBox_5.addItems(version_folders)


    def loadScene(self):
        # Get the folder names from the combo boxes
        project_name = self.comboBox.currentText()
        sequence_name = self.comboBox_2.currentText()
        shot_name = self.comboBox_3.currentText()
        element_name = self.comboBox_4.currentText()
        version_name = self.comboBox_5.currentText()
    
        # Concatenate them with underscores
        final_path = f"{project_name}_{sequence_name}_{shot_name}_{element_name}_{version_name}"
    
        # Construct the full file path
        full_file_path = os.path.join(self.lineEdit.text(), project_name, sequence_name, shot_name, element_name, final_path)
    
        # Normalize the file path (ensure consistent slashes)
        full_file_path = os.path.normpath(full_file_path)
    
        # Check if the file exists before loading it
        if os.path.isfile(full_file_path):
            QtWidgets.QMessageBox.information(None, "Successful", f"Opening Scene:\n{full_file_path}")
            nuke.scriptOpen(full_file_path)  # Load the scene in Nuke
        else:
            QtWidgets.QMessageBox.warning(None, "Error", "Invalid")

    def saveScene(self):
        # Get the selected root directory from the UI
        root_directory = self.lineEdit.text().strip()  # Ensure no extra spaces
    
        # Check if root directory is selected
        if not root_directory:  
            QtWidgets.QMessageBox.warning(None, "Error", "Root directory not selected")
            return  # Stop execution
    
        # Get the current Nuke script name
        current_scene_path = nuke.root().name()  # Full path of the opened scene
        current_scene_name = os.path.basename(current_scene_path)  # Extract only the filename
    
        # Extract project, sequence, shot, element, and version from UI
        project_name = self.comboBox.currentText()
        sequence_name = self.comboBox_2.currentText()
        shot_name = self.comboBox_3.currentText()
        element_name = self.comboBox_4.currentText()
        current_version = self.comboBox_5.currentText()  # Current version from comboBox
    
        # Expected naming convention
        expected_file_name = f"{project_name}_{sequence_name}_{shot_name}_{element_name}_{current_version}.nk"
        expected_folder_path = os.path.join(root_directory, project_name, sequence_name, shot_name, element_name)
    
        # Ensure the save directory exists
        if not os.path.isdir(expected_folder_path):
            QtWidgets.QMessageBox.warning(None, "Error", "Target save directory does not exist.")
            return
    
        # Find existing versions in the folder
        existing_versions = [f for f in os.listdir(expected_folder_path) if f.startswith(f"{project_name}_{sequence_name}_{shot_name}_{element_name}_") and f.endswith(".nk")]
    
        # Extract numerical version numbers
        version_numbers = []
        for file in existing_versions:
            version_part = file.split('_')[-1].split('.')[0]  # Extract 'v0001' part
            if version_part.startswith('v'):
                version_numbers.append(int(version_part[1:]))  # Convert 'v0001' -> 1
    
        # Determine new version number
        if version_numbers:
            new_version = max(version_numbers) + 1  # Get max version and add 1
        else:
            new_version = 1  # If no versions exist, start from v0001
    
        new_version_str = f"v{new_version:04d}"  # Format as 'v0007'
        new_file_name = f"{project_name}_{sequence_name}_{shot_name}_{element_name}_{new_version_str}.nk"
        new_file_path = os.path.join(expected_folder_path, new_file_name)
    
        # Save the file in Nuke
        nuke.scriptSaveAs(new_file_path)
        QtWidgets.QMessageBox.information(None, "Save Successful", f"Scene saved as:\n{new_file_path}")


        self.parent().close()


def show_dialog():
    # Check if a QApplication instance already exists
    app = QtWidgets.QApplication.instance()
    if not app:
        app = QtWidgets.QApplication(sys.argv)

    # Create the dialog
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)

    # Show the dialog
    Dialog.exec_()  # Use exec_() to keep the dialog open


# Run in Nuke's main thread
nuke.executeInMainThread(show_dialog)