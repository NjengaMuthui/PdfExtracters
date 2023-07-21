f = open("txt/answers.txt")

count = 0
lines = f.readlines()

for i in range(1697,1747):
    
    ans = lines[i].replace("\n","").split(",")
    ans  = ans[:-1]
    count += len(ans)
    print("Page {} no. {}".format(i+1,count+2))

   