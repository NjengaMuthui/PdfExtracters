from directory import getPdfFiles
from extract import extractTypeOne
from extract2 import extractType2
from extract5 import extractPdf
import sys
import json

subject = sys.argv[1]

files = getPdfFiles("pdf/Type1/"+subject)
questions = []
problems = []


for file in files:
    questions.extend(extractTypeOne(file))

files2 = getPdfFiles("pdf/Type2/"+subject)

for file in files2:
    questions.extend(extractType2(file))  

files3 = getPdfFiles("pdf/Type3/"+subject)


for file in files3:
    q ,p = extractPdf(file)
    questions.extend(q)
    problems.extend(p)
    print("Number of questions so far = {}".format(len(questions)))
    print("Number of problems so far = {}".format(len(problems)))

all_questions = json.dumps(questions, indent=4)
all_problems = json.dumps(problems, indent=4)


with open("json/{}.json".format(subject), "w") as outfile:
    outfile.write(all_questions)

with open("json/problem_{}.json".format(subject), "w") as outfile:
    outfile.write(all_problems)