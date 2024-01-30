import matplotlib.pyplot as plt
import numpy as np
import json
from datetime import datetime
from datetime import timezone

def timeConvert(dateString):
    return datetime.fromisoformat(
        dateString[:-1]
    ).astimezone(timezone.utc)
 
with open('sample.json') as json_file:
    data = json.load(json_file)

authorDetails = {}

def processData():
    firstCommitDate = ""
    
    # find date of first commit (date of project creation)
    for file in data:
      commits = data.get(file).get('commits')

      for c in commits:
          date = timeConvert(c.get('date'))
          if firstCommitDate == "" or date < firstCommitDate:
              firstCommitDate = date

    print(firstCommitDate)
    # create author data dict
    for i, file in enumerate(data):
        fileData = data.get(file)
        commits = fileData.get('commits')

        for c in commits:
            author = c.get('author')
            date = timeConvert(c.get('date'))

            deltaTime = date - firstCommitDate
            weeksPassed = int(deltaTime.days / 7)

            if author in authorDetails:
                authorDetails[author].append({'fileX': i, 'weeks': weeksPassed})
            else:
                authorDetails[author] = [{'fileX': i, 'weeks': weeksPassed}]

def plotData(x, y, color, author):
    plt.scatter(x, y, c=color, alpha=0.5, label=author)
    return

processData()

for author in authorDetails:
    arr = authorDetails.get(author)
    x = []
    y = []

    for d in arr:
        x.append(d.get('fileX'))
        y.append(d.get('weeks'))

    colors = np.random.rand(3,)

    plotData(x, y, colors, author)

plt.title("File vs Week worked on")
plt.xlabel("File")
plt.ylabel("Weeks")
plt.legend(title="Authors", loc='lower center', bbox_to_anchor=(1.2, 0.0))
plt.show()
