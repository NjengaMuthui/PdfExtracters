import glob

def getPdfFiles(directory):
    return glob.glob("{}/*.pdf*".format(directory))

def getJpgFiles(directory):
   return glob.glob("{}/*.jpg*".format(directory))

def write_to_Json(questions_json,dir):
    with open("jsonn/{}.json".format(dir), "w") as outfile:
      outfile.write(questions_json)
