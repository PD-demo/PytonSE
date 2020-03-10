from tools import Actions
from tools import JsonTools
import time
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-l", "--sourcelanguage", required=True)
ap.add_argument("-r", "--targetlanguage", required=True)
args = vars(ap.parse_args())



jsontools = JsonTools()
actions = Actions()
pom = jsontools.loadjson("pom.json")
if actions.get_current_input_language(pom) != "ENGLISH" or args['sourcelanguage'] != "en":
    source_language = actions.select_source_language(args['sourcelanguage'], pom)
if actions.get_current_target_language(pom) != "ENGLISH" or args['targetlanguage'] != "en":
    target_language = actions.select_target_language(args['targetlanguage'], pom)
time.sleep(2)
actions.swap_language(pom)
time.sleep(2)
if (actions.get_current_input_language(pom) == target_language) and (actions.get_current_target_language(pom) == source_language):
    status = "SUCCESSFUL"
else:
    status = "FAILED"
print("TEST CASE: SWAP_LANGUAGE    STATUS:" + status)
actions.quit_browser()