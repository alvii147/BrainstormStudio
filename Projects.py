from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QDialog,
    QDialogButtonBox,
)
from PyQt5.QtCore import (
    Qt,
)
from PyQt5.QtGui import (
    QPixmap,
    QCursor,
)

from ColorsUtils import visibleFontColor
from Layouts import QFlowLayout

# ----------------------------------------------------------------------
# Project Component Class
# ----------------------------------------------------------------------

class Component:
    def __init__(self, title = 'New Component'):
        self.title = title
        self.technologies = []

    def addTechnology(self, technology):
        self.technologies.append(technology)

# ----------------------------------------------------------------------
# Project Class
# ----------------------------------------------------------------------

class Project:
    def __init__(self, title = 'New Project', description = ''):
        self.title = title
        self.description = description
        self.components = []

    def addComponent(self, component):
        self.components.append(component)

# ----------------------------------------------------------------------
# Project View for one Project
# ----------------------------------------------------------------------

class ProjectView(QWidget):
    def __init__(self, project, iconsData):
        super().__init__()
        self.project = project
        self.iconsData = iconsData
        self.initWidget()

    def initWidget(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f'''
        QWidget {{
            background-color: rgba(255, 255, 255, 20);
        }}
        QWidget:hover {{
            background-color: rgba(255, 255, 255, 55);
        }}
        ''')
        self.vBoxMain = QVBoxLayout()

        self.title = QLabel()
        self.title.setWordWrap(True)
        self.title.setText(self.project.title)
        self.title.setStyleSheet(f'''
            QLabel {{
                color: rgb(102, 179, 255);
                background-color: transparent;
                font-size: 12pt;
                padding-top: 12px;
                padding-bottom: 6px;
            }}
        ''')
        self.vBoxMain.addWidget(self.title)

        self.description = QLabel()
        self.description.setWordWrap(True)
        self.description.setText(self.project.description)
        self.description.setStyleSheet(f'''
            QLabel {{
                color: rgb(255, 255, 255);
                background-color: transparent;
                font-size: 10pt;
            }}
        ''')
        self.vBoxMain.addWidget(self.description)

        for comp in self.project.components:
            hBoxComp = QFlowLayout()
            componentTitle = QLabel()
            componentTitle.setText(comp.title + ':')
            componentTitle.setStyleSheet(f'''
                QLabel {{
                    color: rgb(255, 255, 255);
                    background-color: transparent;
                    font-size: 9pt;
                    padding-right: 5px;
                }}
            ''')

            hBoxComp.addWidget(componentTitle)

            for tech in comp.technologies:
                techWidget = QWidget()
                techWidget.setAttribute(Qt.WA_StyledBackground, True)
                techWidget.setStyleSheet(f'''
                    QWidget {{
                        color: {visibleFontColor(self.iconsData[tech]['color'])};
                        background-color: {self.iconsData[tech]['color']};
                        font-size: 8pt;
                        border: 2px solid rgb(0, 0, 0);
                        border-radius: 18px;
                    }}
                    QWidget:hover {{
                        background-color: {'#BF' + self.iconsData[tech]['color'].lstrip('#')};
                    }}
                ''')

                hBoxTech = QHBoxLayout()

                techIcon = QPixmap('simple-icons/iconspng/' + self.iconsData[tech]['file'].rstrip('.svg') + '.png')
                techIcon = techIcon.scaled(20, 20, Qt.KeepAspectRatio, Qt.FastTransformation)
                techIconLabel = QLabel()
                techIconLabel.setPixmap(techIcon)
                techIconLabel.setStyleSheet(f'''
                    QLabel {{
                        background-color: transparent;
                        border: none;
                    }}
                ''')
                hBoxTech.addWidget(techIconLabel)

                techTitle = QLabel()
                techTitle.setText(tech)
                techTitle.setStyleSheet(f'''
                    QLabel {{
                        color: {visibleFontColor(self.iconsData[tech]['color'])};
                        background-color: transparent;
                        border: none;
                    }}
                ''')
                hBoxTech.addWidget(techTitle)

                techWidget.setLayout(hBoxTech)
                hBoxComp.addWidget(techWidget)

            self.vBoxMain.addLayout(hBoxComp)

        self.setLayout(self.vBoxMain)

    def enterEvent(self, event):
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def leaveEvent(self, event):
        self.setCursor(QCursor(Qt.PointingHandCursor))

# ----------------------------------------------------------------------
# New Project View
# ----------------------------------------------------------------------

class NewProjectView(QDialog):
    def __init__(self, backgroundColorLeft, backgroundColorRight):
        super().__init__()
        #self._width = 350
        #self._height = 400
        self.backgroundColorLeft = backgroundColorLeft
        self.backgroundColorRight = backgroundColorRight
        self.initUI()

    def initUI(self):
        #self.setFixedSize(self._width, self._height)
        self.setWindowTitle("New Project")
        self.setStyleSheet(f'''
            QDialog {{
                background: QLinearGradient(x1:0 y1:0, x2:1 y2:0, stop:0 {self.backgroundColorLeft}, stop:1 {self.backgroundColorRight});
            }}
        ''')

        self.vBoxMain = QVBoxLayout()

        self.projectTitle = QLineEdit()
        self.projectTitle.setStyleSheet(f'''
            QLineEdit {{
                color: rgb(255, 255, 255);
                background-color: rgb(0, 0, 26);
                border-radius: 8px;
                font-size: 11pt;
            }}
        ''')
        self.vBoxMain.addWidget(self.projectTitle)

        self.projectDescription = QTextEdit()
        self.projectDescription.setStyleSheet(f'''
            QTextEdit {{
                color: rgb(255, 255, 255);
                background-color: rgb(0, 0, 26);
                border-radius: 8px;
                font-size: 11pt;
            }}
        ''')
        self.vBoxMain.addWidget(self.projectDescription)

        self.setLayout(self.vBoxMain)