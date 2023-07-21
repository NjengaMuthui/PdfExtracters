from TextOB import Question
import json
import sys

def can_convert_to_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False
    

def clean_text(val):

    arr = val.split(' ')

    for j in range(len(arr) -1 , -1, -1):
        if arr[j] == '':
            del arr[j]


    arr.pop(0)

    ret = arr[0]
    for i in range(1, len(arr)):
        ret += ' '+arr[i]

    return ret        
        

def find_ans(lines, index):

    found = True
    question_array = ['']
    answer = ''
    part = 0
    
    while(found):
        if len(lines[index]) > 4:
            first = lines[index].split()[0]
            if  first == 'Answer':
                found = False
                answer = lines[index+1].split()[0]

            else:
                if first == 'a)' or first == 'b)' or first == 'c)' or first == 'd)':

                    question_array.append(lines[index])
                    part = part + 1

                else:
                    question_array[part] += lines[index]

        index = index + 1
    
    q = Question()
    q.question = clean_text(question_array[0])
    question_array.pop(0)

    for ind in question_array:
        if ind.split()[0] == answer:
            q.answer = clean_text(ind)
        else:
            q.set_choice(clean_text(ind))

    return index , q




file_name = ''
try:
    file_name = sys.argv[1]
except:
    print("Filename not specified")
    exit()     

with open("txt/{}".format(file_name),encoding='utf-8') as file:

    lines = file.readlines()
    
    index = 0

    questions = []

    while index < len(lines):

        if len(lines[index]) > 4:

            ln = lines[index].split()
            val = ln[0]

            if len(val) == 5 and val[4] == '.' and can_convert_to_int(val[:4]):

                index , q = find_ans(lines, index)
                q.source = file_name

                questions.append(q.get_obj())
                
        index  = index + 1

    all_questions = json.dumps(questions, indent=4)

    with open("txt/{}.json".format(file_name), "w") as outfile:
        outfile.write(all_questions)           