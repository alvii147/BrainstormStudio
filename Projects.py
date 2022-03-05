from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QDialog,
    QDialogButtonBox,
    QTreeWidget,
    QTreeWidgetItem,
    QComboBox,
    QSizePolicy,
)
from PyQt6.QtCore import (
    Qt,
)
from PyQt6.QtGui import (
    QPixmap,
    QCursor,
)

from MangoUI import Button, TagBox, FlowLayout
from ColorsUtils import visibleFontColor, brightnessAdjuster

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
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
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
            hBoxComp = FlowLayout()
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
                techWidget.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
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
                techIcon = techIcon.scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.FastTransformation)
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
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def leaveEvent(self, event):
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

# ----------------------------------------------------------------------
# New Project View
# ----------------------------------------------------------------------

class NewProjectView(QDialog):
    def __init__(
        self,
        backgroundColors = {
            'left': 'rgb(50, 50, 50)',
            'right': 'rgb(200, 200, 200)',
        },
        buttonColors = {
            'primary': 'rgb(0, 0, 255)',
            'secondary': 'rgb(0, 0, 0)',
            'background': 'rgb(240, 240, 240)',
        },
        iconsData = {},
    ):
        super().__init__()
        self.backgroundColors = backgroundColors
        self.buttonColors = buttonColors
        self.iconsData = iconsData
        self.initUI()

    def initUI(self):
        self.setWindowTitle('New Project')
        self.setStyleSheet(f'''
            QDialog {{
                background: QLinearGradient(x1:0 y1:0, x2:1 y2:0, stop:0 {self.backgroundColors['left']}, stop:1 {self.backgroundColors['right']});
            }}
        ''')
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.vBoxMain = QVBoxLayout()

        self.projectTitleLabel = QLabel()
        self.projectTitleLabel.setText('Project Title')
        self.projectTitleLabel.setStyleSheet(f'''
            QLabel {{
                color: rgb(255, 255, 255);
                font-size: 11pt;
            }}
        ''')
        self.vBoxMain.addWidget(self.projectTitleLabel)

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

        self.projectDescriptionLabel = QLabel()
        self.projectDescriptionLabel.setText('Project Description')
        self.projectDescriptionLabel.setStyleSheet(f'''
            QLabel {{
                color: rgb(255, 255, 255);
                font-size: 11pt;
            }}
        ''')
        self.vBoxMain.addWidget(self.projectDescriptionLabel)

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

        self.componentTreeLabel = QLabel()
        self.componentTreeLabel.setText('Project Components')
        self.componentTreeLabel.setStyleSheet(f'''
            QLabel {{
                color: rgb(255, 255, 255);
                font-size: 11pt;
            }}
        ''')
        self.vBoxMain.addWidget(self.componentTreeLabel)

        self.componentTree = QTreeWidget()
        self.componentTree.setHeaderHidden(True)
        self.componentTree.setStyleSheet(f'''
            QTreeWidget {{
                color: rgb(255, 255, 255);
                background-color: rgb(0, 0, 26);
                border-radius: 8px;
                font-size: 11pt;
            }}
            QTreeWidget::item:selected:active {{
                color: {self.buttonColors['secondary']};
                background: {self.buttonColors['primary']};
                border: 1px solid rgb(0, 0, 0);
            }}
            QTreeWidget::item:selected:!active {{
                color: {self.buttonColors['secondary']};
                background: {self.buttonColors['primary']};
                border: 1px solid rgb(0, 0, 0);
            }}
            QTreeWidget::item:hover {{
                background: QLinearGradient(x1:0 y1:0, x2:1 y2:0, stop:0 {self.backgroundColors['left']}, stop:1 {self.backgroundColors['right']});
                border: 1px solid rgb(0, 0, 0);
            }}
            QTreeWidget::branch:has-children:!has-siblings:closed,
            QTreeWidget::branch:closed:has-children:has-siblings {{
                border-image: none;
                image: url(img/branch-closed.png);
            }}
            QTreeWidget::branch:open:has-children:!has-siblings,
            QTreeWidget::branch:open:has-children:has-siblings  {{
                border-image: none;
                image: url(img/branch-open.png);
            }}
        ''')
        self.vBoxMain.addWidget(self.componentTree)

        self.hBoxButton = QHBoxLayout()

        self.addComponentButton = Button(
            primaryColor = self.buttonColors['primary'],
            secondaryColor = self.buttonColors['secondary'],
            parentBackgroundColor = self.buttonColors['background'],
            borderWidth = 2,
            borderRadius = 8,
            fontSize = 9,
        )
        self.addComponentButton.setText('Add Component')
        self.addComponentButton.clicked.connect(self.buttonNewComponentClicked)
        self.hBoxButton.addWidget(self.addComponentButton)

        self.editComponentButton = Button(
            primaryColor = self.buttonColors['primary'],
            secondaryColor = self.buttonColors['secondary'],
            parentBackgroundColor = self.buttonColors['background'],
            borderWidth = 2,
            borderRadius = 8,
            fontSize = 9,
        )
        self.editComponentButton.setText('Edit Component')
        self.hBoxButton.addWidget(self.editComponentButton)

        self.vBoxMain.addLayout(self.hBoxButton)

        self.addProjectButton = Button(
            primaryColor = self.buttonColors['primary'],
            secondaryColor = self.buttonColors['secondary'],
            parentBackgroundColor = self.buttonColors['background'],
            borderWidth = 2,
            borderRadius = 8,
            fontSize = 9,
        )
        self.addProjectButton.setText('Add Project')
        self.addProjectButton.clicked.connect(self.buttonAddProjectClicked)
        self.vBoxMain.addWidget(self.addProjectButton)

        self.setLayout(self.vBoxMain)

    def buttonNewComponentClicked(self):
        backgroundColors = self.backgroundColors
        buttonColors = self.buttonColors

        dlg = NewTechnologyView(
            backgroundColors = backgroundColors,
            buttonColors = buttonColors,
            iconsData = self.iconsData,
        )
        exitStatus = dlg.exec()

        if exitStatus == 1:
            compName = dlg.componentName.text()
            techList = dlg.tagbox.tagList

            compItem = QTreeWidgetItem()
            compItem.setText(0, compName)

            for tech in techList:
                techItem = QTreeWidgetItem()
                techItem.setText(0, tech)
                compItem.addChild(techItem)
                
            self.componentTree.addTopLevelItem(compItem)

    def buttonAddProjectClicked(self):
        self.done(1)

class NewTechnologyView(QDialog):
    def __init__(
        self,
        backgroundColors = {
            'left': 'rgb(50, 50, 50)',
            'right': 'rgb(200, 200, 200)',
        },
        buttonColors = {
            'primary': 'rgb(0, 0, 255)',
            'secondary': 'rgb(0, 0, 0)',
            'background': 'rgb(240, 240, 240)',
        },
        iconsData = {},
    ):
        super().__init__()
        self.backgroundColors = backgroundColors
        self.buttonColors = buttonColors
        self.iconsData = iconsData
        self.initUI()

    def initUI(self):
        self.setWindowTitle('New Technology')
        self.setStyleSheet(f'''
            QDialog {{
                background: QLinearGradient(x1:0 y1:0, x2:1 y2:0, stop:0 {self.backgroundColors['left']}, stop:1 {self.backgroundColors['right']});
            }}
        ''')
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.vBoxMain = QVBoxLayout()
        self.vBoxMain.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)

        self.componentNameLabel = QLabel()
        self.componentNameLabel.setText('Component Name')
        self.componentNameLabel.setStyleSheet(f'''
            QLabel {{
                color: rgb(255, 255, 255);
                font-size: 11pt;
            }}
        ''')
        self.vBoxMain.addWidget(self.componentNameLabel)

        self.componentName = QLineEdit()
        self.componentName.setStyleSheet(f'''
            QLineEdit {{
                color: rgb(255, 255, 255);
                background-color: rgb(0, 0, 26);
                border-radius: 8px;
                font-size: 11pt;
            }}
        ''')
        self.vBoxMain.addWidget(self.componentName)

        self.technologiesLabel = QLabel()
        self.technologiesLabel.setText('Technologies')
        self.technologiesLabel.setStyleSheet(f'''
            QLabel {{
                color: rgb(255, 255, 255);
                font-size: 11pt;
            }}
        ''')
        self.vBoxMain.addWidget(self.technologiesLabel)

        self.tagbox = TagBox(
            textColor = self.buttonColors['secondary'],
            backgroundColor = self.buttonColors['primary'],
            backgroundColorOnHover = 'rgb(153, 204, 255)',
        )
        self.tagbox.removeTag = lambda index: self.removeTechnology(index)
        self.vBoxMain.addWidget(self.tagbox)

        self.tagChoice = QComboBox()
        self.tagChoice.setStyleSheet(f'''
            QComboBox {{
                color: rgb(255, 255, 255);
                background-color: rgb(0, 0, 26);
                border-radius: 8px;
                font-size: 11pt;
            }}
            QComboBox QAbstractItemView {{
                color: rgb(255, 255, 255);
                background-color: rgb(0, 0, 26);
                selection-background-color: rgb(0, 0, 77);
                border: 2px solid rgb(255, 255, 255);
            }}
        ''')
        for tech in list(self.iconsData.keys()):
            self.tagChoice.addItem(tech) 
        self.vBoxMain.addWidget(self.tagChoice)

        self.addTechButton = Button(
            primaryColor = self.buttonColors['primary'],
            secondaryColor = self.buttonColors['secondary'],
            parentBackgroundColor = self.buttonColors['background'],
            borderWidth = 2,
            borderRadius = 8,
            fontSize = 9,
        )
        self.addTechButton.setText('Add Technology')
        self.addTechButton.clicked.connect(self.buttonAddTechClicked)
        self.vBoxMain.addWidget(self.addTechButton)

        self.addCompButton = Button(
            primaryColor = self.buttonColors['primary'],
            secondaryColor = self.buttonColors['secondary'],
            parentBackgroundColor = self.buttonColors['background'],
            borderWidth = 2,
            borderRadius = 8,
            fontSize = 9,
        )
        self.addCompButton.setText('Add Component')
        self.addCompButton.clicked.connect(self.buttonAddCompClicked)
        self.vBoxMain.addWidget(self.addCompButton)

        self.setLayout(self.vBoxMain)

    def buttonAddTechClicked(self):
        self.tagbox.addTag(self.tagChoice.currentText())
        self.tagChoice.removeItem(self.tagChoice.currentIndex())

    def buttonAddCompClicked(self):
        self.done(1)

    def removeTechnology(self, index):
        removedTech = self.tagbox.tagList.pop(index)
        self.tagbox.initTagBox()
        self.tagChoice.addItem(removedTech)
        self.tagChoice.model().sort(0)