import sys
import pickle
import json

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy, QScrollArea
from PyQt5.QtCore import Qt, QEasingCurve
from PyQt5.QtGui import QPixmap

from MangoUI import Button, SliderLayout
from ColorsUtils import Hex_to_RGB, visibleFontColor

class Component:
    def __init__(self, title = 'New Component'):
        self.title = title
        self.technologies = []

    def addTechnology(self, technology):
        self.technologies.append(technology)

class Project:
    def __init__(self, title = 'New Project', description = ''):
        self.title = title
        self.description = description
        self.components = []

    def addComponent(self, component):
        self.components.append(component)

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
            hBoxComp = QHBoxLayout()
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
                techIcon = techIcon.scaled(15, 15, Qt.KeepAspectRatio, Qt.FastTransformation)
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
                #techWidget.setFixedHeight(35)
                hBoxComp.addWidget(techWidget)

            hBoxComp.addStretch()
            self.vBoxMain.addLayout(hBoxComp)

        self.setLayout(self.vBoxMain)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self._width = 1200
        self._height = 800
        self._xPos = 400
        self._yPos = 200
        self.loadProjects()
        self.loadIcons()
        self.setColors()
        self.initUI()

    def loadProjects(self):
        self.projectsList = []
        try:
            with open('projectlist.pkl', 'rb') as projectlistfile:
                self.projectsList = pickle.load(projectlistfile)
        except FileNotFoundError:
            self.projectsList = []

    def loadIcons(self):
        with open('simple-icons/iconsLUT.json', 'r') as iconsdatafile:
            self.iconsData = json.load(iconsdatafile)

    def setColors(self):
        self.mainBackgroundColor = 'rgb(0, 0, 26)'

        self.slideBackgroundColorLeft = 'rgb(0, 31, 51)'
        self.slideBackgroundColorRight = 'rgb(41, 0, 51)'

        self.buttonPrimaryColor = 'rgb(102, 179, 255)'
        self.buttonSecondaryColor = 'rgb(0, 0, 26)'

    def initUI(self):
        self.setGeometry(self._xPos, self._yPos, self._width, self._height)
        self.setWindowTitle('Brainstorm Studio')

        self.setStyleSheet(f'''
            QMainWindow {{
                background-color: {self.mainBackgroundColor};
            }}
        ''')

        self.sliderLayout = SliderLayout(
            direction = Qt.Horizontal,
            duration = 500,
            animationType = QEasingCurve.OutQuad,
            wrap = False,
        )

        self.projectsViewSlide = QVBoxLayout()
        self.projectsViewContainer = QWidget()
        self.projectsScrollView = QScrollArea()

        self.slide2 = QHBoxLayout()
        self.container2 = QWidget()

        for prj in self.projectsList:
            tmpprj = ProjectView(prj, self.iconsData)
            self.projectsViewSlide.addWidget(tmpprj)

        self.projectsViewSlide.addStretch()

        self.projectsViewContainer.setLayout(self.projectsViewSlide)
        self.projectsViewContainer.setStyleSheet(f'''
            QWidget {{
                background: QLinearGradient(x1:0 y1:0, x2:1 y2:0, stop:0 {self.slideBackgroundColorLeft}, stop:1 {self.slideBackgroundColorRight});
            }}
        ''')

        self.projectsScrollView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.projectsScrollView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.projectsScrollView.setWidgetResizable(True)
        self.projectsScrollView.setWidget(self.projectsViewContainer)
        self.sliderLayout.addWidget(self.projectsScrollView)

        self.title2 = QLabel()
        self.title2.setText('Where ideas are born')
        self.title2.setStyleSheet(f'''
            QLabel {{
                color: rgb(255, 255, 255);
            }}
        ''')
        self.title2.setAlignment(Qt.AlignCenter)
        self.slide2.addWidget(self.title2)

        self.container2.setLayout(self.slide2)
        self.container2.setStyleSheet(f'''
            QWidget {{
                background: QLinearGradient(x1:0 y1:0, x2:1 y2:0, stop:0 {self.slideBackgroundColorLeft}, stop:1 {self.slideBackgroundColorRight});
            }}
        ''')
        self.sliderLayout.addWidget(self.container2)

        self.buttonProjectsView = Button(
            primaryColor = self.buttonPrimaryColor,
            secondaryColor = self.buttonSecondaryColor,
            parentBackgroundColor = self.mainBackgroundColor,
            borderWidth = 2,
            borderRadius = 8,
            fontSize = 9,
        )
        self.buttonProjectsView.setText('  Projects  ')
        self.buttonProjectsView.clicked.connect(self.sliderLayout.slidePrevious)

        self.buttonBrainstormHub = Button(
            primaryColor = self.buttonPrimaryColor,
            secondaryColor = self.buttonSecondaryColor,
            parentBackgroundColor = self.mainBackgroundColor,
            borderWidth = 2,
            borderRadius = 8,
            fontSize = 9,
        )
        self.buttonBrainstormHub.setText('  Brainstorm Hub  ')
        self.buttonBrainstormHub.clicked.connect(self.sliderLayout.slideNext)

        self.topButtonBarLayout = QHBoxLayout()
        self.topButtonBarLayout.addWidget(self.buttonProjectsView)
        self.topButtonBarLayout.addWidget(self.buttonBrainstormHub)
        self.topButtonBarLayout.addStretch()

        self.vBoxMain = QVBoxLayout()
        self.vBoxMain.addLayout(self.topButtonBarLayout)
        self.vBoxMain.addWidget(self.sliderLayout)

        self.centralWidget = QWidget(self)
        self.centralWidget.setLayout(self.vBoxMain)
        self.setCentralWidget(self.centralWidget)

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = Window()
    sys.exit(app.exec_())