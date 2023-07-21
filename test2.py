from pikepdf import Pdf,Operator
import pikepdf
from TextOB import Ctext,Rect,Question_Block,Question,put_newline_between

def extractType2(file):

    try:
        my_pdf = Pdf.open(file)
    except:
        print("Error opening file named "+file)


    all_questions = []
    page_num = 1
    arr = [9,10,30,31,32]

    for page in arr:

        commands = pikepdf.parse_content_stream(my_pdf.pages[page])
        textblocks = []
        skip = False
        currrent_block = 0
        question_indicators = []
        rects = []
        answer_block = []

        for i  in range(len(commands)):
            if skip:
                if commands[i].operator == Operator('ET'):
                    
                    skip = False
                    currrent_block = currrent_block + 1

                elif commands[i].operator == Operator('rg'):
                    
                    if not (float(commands[i].operands[2]) == 0.0):
                        textblocks[currrent_block].isAnswer = True

                elif commands[i].operator == Operator('Tf'):
                    
                    textblocks[currrent_block].size = float(commands[i].operands[1])

                elif commands[i].operator == Operator('Tm'):
                    textblocks[currrent_block].x = float(commands[i].operands[4])
                    textblocks[currrent_block].Y = float(commands[i].operands[5])

                elif commands[i].operator == Operator('TJ'):
                        con =''
                        for j in range(0,len(commands[i].operands[0]) ,2):
                            con += str(commands[i].operands[0][j])

                        textblocks[currrent_block].value = con        
            else:
                if commands[i].operator == Operator('BT'):
                    skip = True
                    textblocks.append(Ctext())

            if commands[i].operator == Operator('m'):
                if commands[i+3].operator == Operator('l'):
                    rects.append(Rect(float(commands[i+2].operands[1])))
                elif commands[i+1].operator == Operator('l'):
                    answer_block.append(Rect(float(commands[i+1].operands[1])))



        question_blocks = []

        for t in range(len(textblocks)):
            if textblocks[t].size < 8.0:
                if t > 0:
                    if textblocks[t-1].size < 8.0:
                        question_indicators[len(question_indicators)-1] = textblocks[t].Y
                    else:
                        question_indicators.append(textblocks[t].Y)
                        question_blocks.append(Question_Block())
                

        rects.pop(0)
        answer_block.pop(0)
        answer_block.pop(0)
        answers = []
        for index in range(0,len(answer_block),2):
            answers.append(answer_block[index])
        

        first_block = question_indicators[0]

        try:
            second_block = question_indicators[1]
        except:
            second_block = 0.0
        try:
            third_block = question_indicators[2]
        except:
            third_block = 0.0 
        try:
            fourth_block = question_indicators[3]
        except:
            fourth_block = 0.0

        for textblock in textblocks:
            if textblock.x > 80.0 :
                if first_block > textblock.Y and textblock.Y > second_block:
                    question_blocks[0].texts.append(textblock)

                elif second_block > textblock.Y and textblock.Y > third_block:
                    question_blocks[1].texts.append(textblock)

                elif third_block > textblock.Y and textblock.Y > fourth_block:
                    question_blocks[2].texts.append(textblock)

                elif fourth_block > textblock.Y:
                    question_blocks[3].texts.append(textblock)

        for rect in rects:
            if first_block > rect.Y and rect.Y > second_block:
                    question_blocks[0].rects.append(rect)

            elif second_block > rect.Y and rect.Y > third_block:
                    question_blocks[1].rects.append(rect)

            elif third_block > rect.Y and rect.Y > fourth_block:
                    question_blocks[2].rects.append(rect)

            elif fourth_block > textblock.Y:
                question_blocks[3].rects.append(rect)

        for ind,block in enumerate(question_blocks):
            if len(block.rects)>2:
                    
                    q = Question()
                    choices = ['','','','']

                    fir_bloc = block.rects[0].Y + 8.0

                    sec_bloc = block.rects[1].Y + 8.0

                    tri_bloc = block.rects[2].Y + 8.0

                    try:
                        quad_bloc = block.rects[3].Y + 8.0
                    except:
                        quad_bloc = block.rects[2].Y + 8.0

                    for text in block.texts:
    
                            if text.Y > fir_bloc:
                                q.question = put_newline_between(q.question, text.value)

                            elif fir_bloc > text.Y and text.Y > sec_bloc:

                                if fir_bloc > answers[ind].Y and answers[ind].Y > sec_bloc:
                                    q.answer = put_newline_between(q.answer, text.value)
                                else:
                                    choices[0] = put_newline_between(choices[0], text.value) 
                                                    

                            elif sec_bloc > text.Y and text.Y > tri_bloc: 
                                if sec_bloc > answers[ind].Y and answers[ind].Y > tri_bloc:
                                    q.answer = put_newline_between(q.answer, text.value)
                                else:
                                    choices[1] = put_newline_between(choices[1], text.value) 

                            elif tri_bloc > text.Y and text.Y > quad_bloc:
                                
                                if tri_bloc > answers[ind].Y and answers[ind].Y > quad_bloc:
                                    q.answer = put_newline_between(q.answer, text.value)
                                else:
                                    choices[2] = put_newline_between(choices[2], text.value) 
                            else:
                                if quad_bloc > answers[ind].Y :
                                    q.answer = put_newline_between(q.answer, text.value)
                                else:
                                    choices[3] = put_newline_between(choices[3], text.value)
                    for choice in choices:
                        if not (choice == ''):
                            q.set_choice(choice)

                    q.source = file
                                               
                    all_questions.append(q.get_obj())
        page_num += 1

    print("all questions number is: {}".format(len(all_questions)))
    print(all_questions)       
    return all_questions


extractType2("pdf/type2/met/MET.pdf")