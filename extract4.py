
with open("txt/ECQB question bank.txt") as f:
    
    lines = f.readlines()
    for line in lines:
        print(line.decode('utf-8')) 