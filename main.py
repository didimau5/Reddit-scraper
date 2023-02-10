# Personal ID: QvlqmD9y82pMuqF8-Tlnzg
# Secret: zcOC98I6gN58udQuNESv0JEWvoCE8w
import time
import csv
import praw
import pandas as pd

df = pd.read_csv(r'C:\Users\didac\OneDrive\Escritorio\Specification report!\LicensedCarsDataset.csv',
                             low_memory=False)

listOfElems = df.GenModel.unique()


def write_data(redditValues):
    with open('RedditData.csv', 'a', encoding='UTF8', newline='\n') as f:
        writer = csv.writer(f, delimiter=',', lineterminator='\n')
        writer.writerow(redditValues)


def getIndexes(df, car):
    listOfCars = list()
    result = df.isin([car])
    seriesObject = result.any()
    columnNames = list(seriesObject[seriesObject == True].index)
    for col in columnNames:
        rows = list(result[col][result[col] == True].index)
        for row in rows:
            listOfCars.append((row, col))
    return listOfCars


dictOfPos = {elem: getIndexes(df, elem) for elem in listOfElems}
totalCarsLicensed = 0
dictofCars = {}
for key, value in dictOfPos.items():
    totalOfCars = 0

    for each in value:
        totalOfCars = totalOfCars + df.at[int(each[0]), 'Licensed']
    totalCarsLicensed += totalOfCars
    if "MISSING" in key:
        continue
    dictofCars[key] = (totalOfCars / 37963646)


reddit = praw.Reddit(client_id='QvlqmD9y82pMuqF8-Tlnzg',
                     client_secret='zcOC98I6gN58udQuNESv0JEWvoCE8w',
                     username='Car_scrap',
                     password='Password123',
                     user_agent='alright')

sentenceslist = []
for i in dictofCars.keys():
    sentenceslist.append(i)
    print(f'Searching now for: {i}')
    blob = ""
    for submission in reddit.subreddit('all').search(i, limit=50):
        print(submission.title)
        blob = blob + " " + submission.title
    sentenceslist.append(blob)
    write_data(sentenceslist)
    sentenceslist.clear()
