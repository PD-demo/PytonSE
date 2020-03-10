from tools import JsonTools
import os

jsontools=JsonTools()
testrun=jsontools.loadjson("testrun.json")
for test in testrun:
    call = "python Tests\\"+ test["test_name"] +".py"
    for arg in test["args"]:
        #print((test["args"])[arg])
      call+=" --"+arg+"="+(test["args"])[arg]
    os.system(call)