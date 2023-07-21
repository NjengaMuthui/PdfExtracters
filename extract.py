from pikepdf import Pdf,Operator
import pikepdf
from TextOB import Rect,TextBlock,Text,Question,put_newline_between

def extractTypeOne(file_name):
     
    try:
        my_pdf = Pdf.open(file_name)
        print("Opening "+file_name)
    except:
        print("Error opening file named "+file_name)    
    

    #if item.operator == Operator('TJ'):
    #        con =''
    #        for i in range(0,len(item.operands[0]) ,2):
    #             con += str(item.operands[0][i])
    #
    #        print(con)
    all_questions = []
    for page in my_pdf.pages:
        items = pikepdf.parse_content_stream(page)
        textblocks = []
        rects = []
        circle = 0.00 
        skip = False
        currrent_block = 0

        cur_loc =  0.00


        for item in items:

            if skip:
                if item.operator == Operator('ET'):
                        skip = False
                        currrent_block = currrent_block + 1

                elif item.operator == Operator('TD'):
                    cur_loc += float(item.operands[1])

                elif item.operator == Operator('TJ'):
                    con =''
                    for i in range(0,len(item.operands[0]) ,2):
                        con += str(item.operands[0][i])

                    textblocks[currrent_block].block.append(Text(cur_loc,con))

                elif item.operator == Operator('Tj'):
                    textblocks[currrent_block].block.append(Text(cur_loc,str(item.operands[0])))     
            else:
                if item.operator == Operator('BT'):
                    skip = True
                    textblocks.append(TextBlock())
                    cur_loc = 0.00

            if item.operator == Operator('m'):
                circle = item.operands[1]

            if item.operator == Operator('re'):
                rects.append(Rect(item.operands[1]))

        textblocks.pop(0)
        textblocks.pop(len(textblocks)-1)
        textblocks[0].block.pop(0)

        upper_bound = float(rects[0].Y) + 8.0

        second_bound = float(rects[1].Y) + 8.0

        third_bound = float(rects[2].Y) + 8.0
        try:
            fourth_bound = float(rects[3].Y) + 8.0
        except:
            fourth_bound = third_bound = float(rects[2].Y) + 8.0    

        answer_bound = float(circle) - 8.0

        question = ''
        answer = ''

        choices = ['','','','']

        for bl in textblocks:
            for txt in bl.block:
                if txt.Y > upper_bound:
                    question =  put_newline_between(question, txt.value)                  

                elif txt.Y < upper_bound and txt.Y > second_bound:
                    if  answer_bound < upper_bound and answer_bound > second_bound:
                            answer =  put_newline_between(answer, txt.value)
                    else:
                            choices[0] = put_newline_between(choices[0], txt.value)

                elif txt.Y < second_bound and txt.Y > third_bound:
                    if answer_bound < second_bound and answer_bound > third_bound:
                            answer =  put_newline_between(answer, txt.value)
                    else:
                            choices[1] = put_newline_between(choices[1], txt.value)

                elif txt.Y < third_bound and txt.Y > fourth_bound:
                    if answer_bound < third_bound and answer_bound > fourth_bound:
                            answer = put_newline_between(answer, txt.value)
                    else:
                            choices[2] = put_newline_between(choices[2], txt.value)
                else:
                    if fourth_bound > answer_bound:
                            answer = put_newline_between(answer, txt.value)
                    else:
                            choices[3] = put_newline_between(choices[3], txt.value)


        q = Question()
        q.question = question
        q.source = file_name
        q.answer = answer
        for choice in choices:
            if not (choice == ''):
                q.set_choice(choice)
        all_questions.append(q.get_obj())          


    
    return all_questions