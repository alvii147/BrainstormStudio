import sys
import pickle
import json

from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QScrollArea,
)
from PyQt5.QtCore import (
    Qt,
    QEasingCurve,
)

from MangoUI import Button, Slider
from ColorsUtils import Hex_to_RGB, visibleFontColor
from Projects import Component, Project, ProjectView, NewProjectView

# ----------------------------------------------------------------------
# Main Window
# ----------------------------------------------------------------------

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self._width = 1200
        self._height = 800
        self._xPos = 400
        self._yPos = -900
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

        self.slider = Slider(
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
        self.slider.addWidget(self.projectsScrollView)

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
        self.slider.addWidget(self.container2)

        self.buttonProjectsView = Button(
            primaryColor = self.buttonPrimaryColor,
            secondaryColor = self.buttonSecondaryColor,
            parentBackgroundColor = self.mainBackgroundColor,
            borderWidth = 2,
            borderRadius = 8,
            fontSize = 9,
        )
        self.buttonProjectsView.setText('  Projects  ')
        self.buttonProjectsView.clicked.connect(self.slider.slidePrevious)

        self.buttonBrainstormHub = Button(
            primaryColor = self.buttonPrimaryColor,
            secondaryColor = self.buttonSecondaryColor,
            parentBackgroundColor = self.mainBackgroundColor,
            borderWidth = 2,
            borderRadius = 8,
            fontSize = 9,
        )
        self.buttonBrainstormHub.setText('  Brainstorm Hub  ')
        self.buttonBrainstormHub.clicked.connect(self.slider.slideNext)

        self.buttonNewProject = Button(
            primaryColor = self.buttonPrimaryColor,
            secondaryColor = self.buttonSecondaryColor,
            parentBackgroundColor = self.mainBackgroundColor,
            borderWidth = 2,
            borderRadius = 8,
            fontSize = 9,
        )
        self.buttonNewProject.setText('  New Project +  ')
        self.buttonNewProject.clicked.connect(self.buttonNewProjectClicked)

        self.topButtonBarLayout = QHBoxLayout()
        self.topButtonBarLayout.addWidget(self.buttonProjectsView)
        self.topButtonBarLayout.addWidget(self.buttonBrainstormHub)
        self.topButtonBarLayout.addStretch()
        self.topButtonBarLayout.addWidget(self.buttonNewProject)

        self.vBoxMain = QVBoxLayout()
        self.vBoxMain.addLayout(self.topButtonBarLayout)
        self.vBoxMain.addWidget(self.slider)

        self.centralWidget = QWidget(self)
        self.centralWidget.setLayout(self.vBoxMain)
        self.setCentralWidget(self.centralWidget)

        self.show()

    def buttonNewProjectClicked(self):
        backgroundColors = {
            'left': self.slideBackgroundColorLeft,
            'right': self.slideBackgroundColorRight,
        }

        buttonColors = {
            'primary': self.buttonPrimaryColor,
            'secondary': self.buttonSecondaryColor,
            'background': self.mainBackgroundColor,
        }

        dlg = NewProjectView(
            backgroundColors = backgroundColors,
            buttonColors = buttonColors,
            iconsData = self.iconsData,
        )
        exitStatus = dlg.exec()

        if exitStatus == 1:
            prj = Project(
                title = dlg.projectTitle.text(),
                description = dlg.projectDescription.toPlainText(),
            )

            rootItem = dlg.componentTree.invisibleRootItem()
            for i in range(rootItem.childCount()):
                compItem = rootItem.child(i)
                comp = Component(title = compItem.text(0))

                for j in range(compItem.childCount()):
                    techItem = compItem.child(j)
                    comp.addTechnology(techItem.text(0))

                prj.addComponent(comp)

            self.projectsList.append(prj)
            with open('projectlist.pkl', 'wb') as projectlistfile:
                pickle.dump(self.projectsList, projectlistfile, pickle.HIGHEST_PROTOCOL)

            self.initUI()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = Window()
    sys.exit(app.exec_())