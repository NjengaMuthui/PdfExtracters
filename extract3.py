from pikepdf import Pdf,Operator
import pikepdf
import json

file = "pdf/ECQB question bank.pdf"

try:
    my_pdf = Pdf.open(file)
except:
     print("Error opening file named "+file)
     exit()

choices = []    

for page in  range(100):
#def rangeCall(page):

     commands = pikepdf.parse_content_stream(my_pdf.pages[page])

     for i in range(len(commands)):
          if commands[i].operator == Operator('RG'):
               items = commands[i+3].operands[0]
               try:
                    if items[0] == 'A' or items[0] == 'B' or items[0] == 'C' or items[0] == 'D':
                         if items[2] == ')':
                              choices.append(str(items[0]))
               except:
                    print("error")
#rangeCall(1791)                     

print(len(choices))
answers_json = json.dumps(choices)

with open("json/answers.json".format(), "w") as outfile:
    outfile.write(answers_json)
