import pandas as pd
from zipfile import ZipFile
  
# specifying the zip file name 
SUBMISSION = "sample-submission.zip"

try:
    # opening the zip file in READ mode 
    zipSet = set()
    with ZipFile(SUBMISSION, 'r') as zipObj:
        for entry in zipObj.infolist():
            zipSet.add(entry.filename)

    DIRS = ['code/', 'solution/', 'solution/solution.csv']

    errors = 0
    for filename in DIRS:
        if filename not in zipSet:
            print(f'[ERROR] {filename} is missing in your zip file.')
            errors += 1

    COLS = ['id', 'answer']
    if errors == 0:
        with ZipFile(SUBMISSION, 'r') as zipObj:
            with zipObj.open('solution/solution.csv', 'r') as file:
                solution = pd.read_csv(file)
                fileCols = solution.columns.values.tolist()
                for col in COLS:
                    if col not in fileCols:
                        print(f'[ERROR] {col} column is missing in your solution.csv file.')
                        errors += 1

    if errors == 0:
        print('Congratulations! Submission structure check passed!')
    else:
        print('Please check your submission structure carefully.')
    
except Exception as e:
    print(f'[ERROR] {e}')
