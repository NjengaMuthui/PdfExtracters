from pikepdf import Pdf,Operator
import pikepdf
import pytesseract
import fitz
from PIL import Image
import io
from TextOB import Question,Problem

def extractPdf(file):
     questions = []
     problems = []

     try:

          my_pdf = Pdf.open(file)
          pdf_file = fitz.open(file)
          print("Opening File name: {}".format(file))

     except:
          print("Error opening file named "+file)
          return questions, problems

     for num in range(len(my_pdf.pages)):
          
          try:
               page = my_pdf.pages[num]
               commands = pikepdf.parse_content_stream(page)

               if len(commands)>27:
                    if commands[26].operator == Operator("Tj"):
                         if str(commands[26].operands[0]) == "Candidate:": 

                              image_names = []
                              count = 0
                              found_index = 0

                              for i, command in enumerate(commands):
                                   if command.operator == Operator("Do"):
                                        #print("X:{} Y:{}".format(commands[i-1].operands[4],commands[i-1].operands[5]))
                                        if float(commands[i-1].operands[4]) > 40.0 and float(commands[i-1].operands[5]) > 50.0 and float(commands[i-1].operands[5]) < 500.0:  
                                             try:
                                                  image_names.append( str(command.operands[0])[1:])
                                                  count = count +1          
                                             except:
                                                  print("This is not an image {}".format(command.operands[0]))

                                   if command.operator == Operator("m"):

                                        if commands[i+1].operator == Operator("c"):
                                             found_index = count        


                              image_list  = pdf_file[num].get_images()
                              imagexref = []


                              for name in image_names:
                                   for ref in image_list:
                                        if ref[7] == name:
                                             imagexref.append(ref[0])
                                             break
                              q = Question()
                              q.source = file


                              for i in  range(len(imagexref)):

                                   image_Obj = pdf_file.extract_image(imagexref[i])
                                   image = Image.open(io.BytesIO(image_Obj['image']))
                                   text =  pytesseract.image_to_string(image=image)

                                   if i == 0:
                                        q.question = text

                                   elif i == found_index:
                                        q.answer = text
                                        
                                   else:
                                        q.set_choice(text)

                              if q.question == "" or q.answer == "" or q.choiceone == "" or q.choicetwo == "":
                              
                                   p = Problem(file, num)
                                   p.question = q.question
                                   p.answer = q.answer
                                   p.choiceone = q.choiceone
                                   p.choicetwo = q.choicetwo
                                   p.choicethree = q.choicethree
                                   problems.append(p.get_obj())
                              
                              else:
                                   questions.append(q.get_obj())
          except:
               print("Error in page {}".format(num))                         


     return questions, problems