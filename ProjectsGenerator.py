import pickle
from BrainstormStudio import Project, Component

backend = Component(title = 'Backend')
backend.addTechnology('Python')
backend.addTechnology('Django')

frontend = Component(title = 'Frontend')
frontend.addTechnology('JavaScript')
frontend.addTechnology('React')
frontend.addTechnology('React Router')
frontend.addTechnology('Redux')

database = Component(title = 'Database')
database.addTechnology('PostgreSQL')
database.addTechnology('Amazon AWS')
database.addTechnology('Amazon S3')

todoproject = Project(
    title = 'TO-DO application',
    description = 'Program to keep track of tasks the user needs to do. Tasks can have subtasks within them. There will be a progress bar display beside each task, indicating the level of completeness of that task. Each task/subtask may be ticked off by user to indicate completeness.')
todoproject.addComponent(backend)
todoproject.addComponent(frontend)
todoproject.addComponent(database)

machinelearning = Component(title = 'Machine Learning')
machinelearning.addTechnology('Python')
machinelearning.addTechnology('Jupyter')
machinelearning.addTechnology('NumPy')
machinelearning.addTechnology('Numba')
machinelearning.addTechnology('Keras')
machinelearning.addTechnology('TensorFlow')
machinelearning.addTechnology('pandas')
machinelearning.addTechnology('scikit-learn')
machinelearning.addTechnology('SciPy')
machinelearning.addTechnology('PyTorch')
machinelearning.addTechnology('Apache Spark')
machinelearning.addTechnology('OpenCV')
machinelearning.addTechnology('Kaggle')

backend = Component(title = 'Backend')
backend.addTechnology('Python')
backend.addTechnology('Flask')

frontend = Component(title = 'Frontend')
frontend.addTechnology('HTML5')
frontend.addTechnology('CSS3')
frontend.addTechnology('JavaScript')

database = Component(title = 'Database')
database.addTechnology('MySQL')
database.addTechnology('Google Cloud')

maskdetectionproject = Project(
    title = 'Mask Detection using Computer Vision',
    description = 'Machine learning application that can detect face masks. It should also be able to detect incorrectly worn masks.')
maskdetectionproject.addComponent(machinelearning)
maskdetectionproject.addComponent(backend)
maskdetectionproject.addComponent(frontend)
maskdetectionproject.addComponent(database)

projectlist = [todoproject, maskdetectionproject]

with open('projectlist.pkl', 'wb') as projectlistfile:
    pickle.dump(projectlist, projectlistfile, pickle.HIGHEST_PROTOCOL)