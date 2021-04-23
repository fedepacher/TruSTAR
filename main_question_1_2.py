""" 
The main_question_1_2.py file attemp to solve TruStar Software Engineering Questionnaire

1- Write a function that allows you to extract valuable information from a string representing a
json object. The input of the function is a string that contains a json object, and an array of
properties and sub-properties (using dot notation).
The output of the function is a dictionary containing the values of each one of the matching
properties. If the property or sub-property is not present, the entry doesn't show up in the result.
For example, if the inputs are (written in multiple lines for clarity)
a=' {
    "guid": "1234",
    "content": {
                "type": "text/html",
                "title": "Challenge 1",
                "entities": [ "1.2.3.4", "wannacry", "malware.com"]
                },
    "score": 74,
    "time": 1574879179
}'
b = ["guid", "content.entities", "score", "score.sign"]

> f(a,b)
> { "guid": "1234", "content.entities": [ "1.2.3.4", "wannacry", "malware.com"], "score": 74}

2- If not done already, modify the function above to accept an arbitrarily nested sequence of
properties (e.g "
content.link.href.parent"​ )
"""


import json
from extractor import json_interpreter

#json object given as example
a = '{"guid": "1234", "nono": {"type": "text/html", "title": "Challenge 1", "entities": [ "1.2.3.4", "wannacry", "malware.com"]}, "content": {"type": "text/html", "title": "Challenge 1", "entities": [ "1.2.3.4", "wannacry", "malware.com"]}, "score": 74, "time": 1574879179}'
b = ["guid", "content.entities", "score", "content.link.href.parent", "score.sign"]


dic = { }
for prop in b:                                                              #go through input data list
    value = json_interpreter(json.loads(a), prop)     #search value
    if len(value) > 0:                                                      #if value lenght = 0 no value was found
        dic.update({ prop : value[0] })
print(dic)




