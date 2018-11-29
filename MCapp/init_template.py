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

#Initial Template. I replaced it with json from raw_template to make creating various templates faster
# t = {}
# t["cost"] = {"x1": 990, "x2": 1120, "y1": 600, "y2": 630}
# t["tax"] = {"x1": 990, "x2": 1120, "y1": 676, "y2": 705}
# t["total"] = {"x1": 990, "x2": 1120, "y1": 790, "y2": 820}
#
#
# t["address_line1"] = {"x1": 120, "x2": 500, "y1": 328, "y2": 358}
# t["address_line2"] = {"x1": 120, "x2": 500, "y1": 370, "y2": 400}
#
# t["city"] = {"x1": 120, "x2": 360, "y1": 406, "y2": 444}
# t["post_code"] = {"x1": 120, "x2": 310, "y1": 446, "y2": 480}

# print(templateDictionary)
# crop.save_template(templateDictionary, sys.argv[1])
