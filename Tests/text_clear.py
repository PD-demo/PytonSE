from tools import Actions
from tools import JsonTools
import time
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--sourcetext", required=True)
args = vars(ap.parse_args())
text = args["sourcetext"]

jsontools = JsonTools()
actions = Actions()
pom = jsontools.loadjson("pom.json")

actions.input_source_text(text, pom)
time.sleep(2)
#if actions.check_empty_translation(pom) != "":
actions.clear_input(pom)
time.sleep(2)
if actions.check_empty_translation(pom) == "":
    status = "SUCCESSFUL"
else:
    status = "FAILED"
print("TEST CASE: TEXT_CLEANUP    STATUS:" + status)
actions.quit_browser()