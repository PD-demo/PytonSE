from tools import Actions
from tools import JsonTools
import time
import os
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-r", "--targetlanguage", required=True)
ap.add_argument("-f", "--sourcefile", required=True)
ap.add_argument("-o", "--validationfile", required=True)
args = vars(ap.parse_args())

jsontools = JsonTools()
actions = Actions()
pom = jsontools.loadjson("pom.json")
base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
source_path = base_path + "\\" + args['sourcefile']
target_path = base_path + "\\" + args['validationfile']
actions.set_doc_translation(pom)
if actions.get_current_target_language(pom) != "ENGLISH" or args['targetlanguage'] != "en":
    target_language = actions.select_target_language(args['targetlanguage'], pom)
actions.upload_text_file(source_path, pom)
result = actions.translate_text_file(pom)
time.sleep(2)
target="".join(open(target_path, "r").readlines())
if result == str(target).upper():
    status = "SUCCESSFUL"
else:
    status = "FAILED"
print("TEST CASE: MANUAL_PICKER    STATUS:" + status)
actions.quit_browser()