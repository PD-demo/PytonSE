from tools import Actions
from tools import JsonTools
import time
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-r", "--targetlanguage", required=True)
ap.add_argument("-s", "--sourcetext", required=True)
ap.add_argument("-v", "--validationtext", required=True)
args = vars(ap.parse_args())
text = args["sourcetext"]
translation = args["validationtext"]


jsontools = JsonTools()
actions = Actions()
pom = jsontools.loadjson("pom.json")
temp = actions.select_source_language("ru", pom)
actions.set_autodetect_language(pom)
time.sleep(2)
if actions.get_current_target_language(pom) != "ENGLISH" or args['targetlanguage'] != "en":
    temp = actions.select_target_language(args['targetlanguage'], pom)
actions.input_source_text(text, pom)
time.sleep(2)
if actions.get_target_text(pom) == translation.upper():
    status = "SUCCESSFUL"
else:
    status = "FAILED"
print("TEST CASE: LANGUAGE_AUTODETECT    STATUS:" + status)
actions.quit_browser()
