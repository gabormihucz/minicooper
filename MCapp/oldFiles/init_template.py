import json
import sys
import pickle

#function that takes CLA, loads related json from rawTemplates and save a pickle of it
def load_and_save(templateName):
    with open("rawTemplates/"+sys.argv[1]+".json","r") as template:
        templateDictionary = json.loads(template.read())

    with open("templates/" + sys.argv[1] + ".pkl", "wb") as f:
        pickle.dump(templateDictionary, f, pickle.HIGHEST_PROTOCOL)

#main fns
load_and_save(sys.argv[1])
