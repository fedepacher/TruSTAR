""" 
The main_question_3.py file attemp to solve TruStar Software Engineering Questionnaire

3- Modify the function above to allow accessing arrayed properties. For example:

> f(a,["guid", "content.entities[0]")
> { "guid": "1234", "content.entities[0]": "1.2.3.4"}

If the property is not arrayed or the index is not found, there's no need to generate an output for
it. Consider that the array access can happen in the middle of the property chain (for example:
"content.entities[0].time"​ )
"""

import json
from extractor import json_interpreter
 

#json object given as example
a = '{"guid": "1234", "nono": {"type": "text/html", "title": "Challenge 1", "entities": [ "1.2.3.4", "wannacry", "malware.com"]}, "content": {"type": "text/html", "title": "Challenge 1", "entities": [ "1.2.3.4", "wannacry", "malware.com", {"time": 365468}]}, "score": 74, "time": 1574879179}'
b = ["content.entities[3].time", "content.entities[0]", "guid", "content.entities", "loco.entities", "score", "content.link.href.parent", "score.sign"]


dic = { }
try:
    for prop in b:                                                              #go through input data list
        value = json_interpreter(json.loads(a), prop)                           #search value
        if len(value) > 0:                                                      #if value lenght = 0 no value was found
            dic.update({ prop : value[0] })
except ValueError:
    print("Not valid JSON data")       
print(dic)




