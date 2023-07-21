import sys
from extract5 import extractPdf
import json
import sys
from directory import getPdfFiles

try:
    directory = sys.argv[1]
except:
    print("Invalid directory")
    exit()     

working_dir = "Completed/"
questions = []
problems = []

for file in getPdfFiles(working_dir+directory):
    
    q , p = extractPdf(file)
    questions.extend(q)
    problems.extend(p)

out = json.dumps(questions, indent=4)


with open(working_dir+"jsonn/{}.json".format(directory),"w") as fl:
    fl.write(out)