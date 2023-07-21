def put_newline_between(value,line):
     if not (value == ''):
          value += '\n'
     value += line
     return value

class Text:
    def __init__(self, y ,val):
      self.Y = y
      self.value = val

    def __repr__(self):
      return "location{}  \n {}".format(self.Y, self.value)

class Question_Block:
    def __init__(self):
        self.texts = []
        self.rects = []
    def print_values(self):
        print("Begining ")
        print(self.texts)
        print(self.rects)
        print("The End ")    

class Ctext(Text):
    def __init__(self, y, val, v):
        super().__init__(y, val)       
        self.isAnswer = v

    def __init__(self):
        super().__init__(0.00, "")
        self.isAnswer = False
        self.size = 0.0
        self.x = 0.0

    def __repr__(self):
      return "{} :is Answer {} size is {} location ({},{})\n".format(self.value, self.isAnswer,self.size,self.x,self.Y)
    

class TextBlock:
    def __init__(self):
        self.block = []
    def __repr__(self):
        all_txt = ''
        for txt in self.block:
            all_txt += txt 
        return all_txt


class Rect:
    def __init__(self, y):
        self.Y = y
    def __str__(self):
        return 'y value is {}'.format(self.Y)
    def __repr__(self):
        return 'y value is {}'.format(self.Y)       

class Question:
    def __init__(self):

        self.question =''
        self.answer = ''
        self.choiceone = ''
        self.choicetwo = ''
        self.choicethree = ''
        self.num = 1
        self.source = ''

    def __repr__(self):
        if self.choicethree == "":
            return 'Question: {} \n answer :{} \n choice :{} \n choice :{}'.format(self.question,self.answer,self.choiceone,self.choicetwo)
        else:
            return 'Question: {} \n answer :{} \n choice :{} \n choice :{} \n choice :{} \n'.format(self.question,self.answer,self.choiceone,self.choicetwo,self.choicethree)
                
    def get_obj(self):
        if self.choicethree == "":
            return  {
            "question":self.question,
            "answer":self.answer,
            "choiceone":self.choiceone,
            "choicetwo":self.choicetwo,
            "source":self.source
        }
        else:
            return  {
            "question":self.question,
            "answer":self.answer,
            "choiceone":self.choiceone,
            "choicetwo":self.choicetwo,
            "choicethree":self.choicethree,
            "source":self.source
        }

        
    def set_choice(self, choice):
        match self.num:
            case 1:
                self.choiceone = choice
                self.num += 1
            case 2:
                self.choicetwo = choice
                self.num += 1
            case 3:
                self.choicethree = choice
                self.num += 1

class Problem(Question):
    def __init__(self, file, num):
        super().__init__()
        self.file_name = file
        self.file_num = num
    def get_obj(self):
        if self.choicethree == "":
            return  {
            "question":self.question,
            "answer":self.answer,
            "choiceone":self.choiceone,
            "choicetwo":self.choicetwo,
            "file_name":self.file_name,
            "question_number":self.file_num
        }
        else:
            return  {
            "question":self.question,
            "answer":self.answer,
            "choiceone":self.choiceone,
            "choicetwo":self.choicetwo,
            "choicethree":self.choicethree,
            "file_name":self.file_name,
            "question_number":self.file_num
        }    


class Line:
    def __init__(self, x , y):
        self.X = x
        self.Y = y
    def __str__(self):
        return 'x value is {} while y vlue is {}'.format(self.X, self.Y)  
    def __repr__(self):
        return 'x value is {} while y value is {}'.format(self.X, self.Y)  