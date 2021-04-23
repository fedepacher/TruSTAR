""" 
The main_question_4.py file attemp to solve TruStar Software Engineering Questionnaire

4- The MITRE organization maintains and publishes a catalog of different cyber entities that we
use extensively at TruSTAR. Their repository is publicly accessible at https://github.com/mitre/cti​.

For this portion of the questionnaire, we ask you to build a full program that, using the function
above and other libraries of choice (anything that allows you to browse directories and files on a
git repo), extracts and outputs the following fields of interest from all the json files found under
the given path.

Path: ​ https://github.com/mitre/cti/enterprise-attack/attack-pattern
Fields: ["id", "objects[0].name", "objects[0].kill_chain_phases"]
"""

import json, requests, time, os
from extractor import json_interpreter


class Main:
    #global data containes in txt files
    RAW_REPOSITORY = ''
    BRANCH = ''
    DIRECTORY = ''
    EXTENSION_JSON = ''
    FILE_PATH = ''
    FILE_NAME = ''
    FILE_EXT_TXT  = ''
    RAW_URL = ''
    URL = ''
    def __init__(self):
        pass
    
    """
    Get file extension
    param content :     content from url git repo 
    param start_index : start index in the content to find where extension begin 
    param end_index :   end index where extension ends
    return bool :       true if extension is the desire extension
    """
    def getextension(self, content, start_index, end_index):
        result = False
        extension = content[start_index : end_index : ]
        if extension == self.EXTENSION_JSON:
            return True
        return False

    """
    Create a file list in specific folder that contain json files name gets from specific git repo
    param content :     content from url git repo 
    return 1
    """
    def createfilelist(self, content):
        if not os.path.exists(self.FILE_PATH):
            os.makedirs(self.FILE_PATH)
        path_txt = os.path.abspath(self.FILE_PATH) 
        files_txt = os.listdir(path_txt)                                                    #get file list
        for item in files_txt:
            if item.endswith(self.FILE_EXT_TXT):
                os.remove(os.path.join(path_txt, item))                                     #delete all file            

        while len(content) > 0:
            var_ind = int(content.find(self.DIRECTORY))
            start_index =  var_ind + len(self.DIRECTORY)
            if start_index >= len(content) or var_ind < 0:
                break
            content = content[start_index : len(content) : ]                                #delete unused content
            filename = ''
            for index in range(len(content)):
                caracter = content[index]
                if caracter == ".":
                    if self.getextension(content, index, index + len(self.EXTENSION_JSON)):
                        with open(os.path.join(self.FILE_PATH, self.FILE_NAME), 'a') as f:
                            f.write(filename + self.EXTENSION_JSON + '\n')
                        break
                filename += caracter
        return 1

    """
    Get request from url
    param url :     url 
    return resp :   return response from url
    """
    def getrequests(self, url):
        resp = ''
        while resp == '':
            try:
                resp = requests.get(url)
                break
            except:
                print("Connection refused by the server..")
                time.sleep(5)
                continue
        return resp

    """
    Open file
    param filename :    file name 
    return lines :      return dictionary of read lines
    """
    def openfile(self, filename):
        try:
            with open(filename, 'r') as txt_file:                                #get all information
                lines = txt_file.readlines()
        except:
            print("No " + filename + " was found")
            exit(1)

        return lines

    """
    Open file
    param filename :    file name 
    return lines :      return list of read lines
    """
    def openfile_retlist(self, filename):
        lines = self.openfile(filename)
        listToStr = ' '.join([str(elem) for elem in lines])                             #convert list to str
        file_list = listToStr.split(',')
        return file_list

    
    """
    Print properties from url data
    return 1      
    """
    def showproperties(self, json_data, properties):
        dic = { }
        try:
            for prop in properties:                                   #go through input data list
                value = json_interpreter(json_data, prop)                    #search value
                if len(value) > 0:                                      #if value lenght = 0 no value was found
                    dic.update({ prop : value[0] })
        except ValueError:
            print("Not valid JSON data")       
        print(dic)
        return 1

    """
    Run function, execute program
    return 1      
    """
    def run(self):
        file_list = self.openfile_retlist('info.txt')

        #get parameters frome info.txt
        self.URL = file_list[0]
        self.RAW_REPOSITORY = file_list[1]
        self.BRANCH = file_list[2]
        self.DIRECTORY = file_list[3]
        self.EXTENSION_JSON = file_list[4]
        self.FILE_PATH = file_list[5]
        self.FILE_NAME = file_list[6]
        self.FILE_EXT_TXT  = file_list[7]
        self.RAW_URL = self.RAW_REPOSITORY + self.BRANCH + self.DIRECTORY
        self.URL += self.BRANCH + self.DIRECTORY
       
        print()
        print('Getting json file from ' + self.URL)
        print()
        print('Please wait...')
        print()
        resp = self.getrequests(self.URL)                                   #get response from url

        content = str(resp.content)
        self.createfilelist(content)                                        #create file list with json names              
        print('-----------------BEGIN-----------------')
        print()
        print('Json filename´s list created in ' + self.FILE_PATH + ' folder')
        print()
        print('Extracting information')
        print()

        read_lines = self.openfile(self.FILE_PATH + '/' + self.FILE_NAME)   #read file to extract all names


        propety_list = self.openfile_retlist('prop_file.txt')               #get properties to be shown 
        
        #extract properties from json array
        for line in read_lines:
            url = self.RAW_URL + line[:-1]                                  #remove last character \n
            resp = self.getrequests(url)
            try:
                data = json.loads(resp.text)           
                self.showproperties(data, propety_list)            
            except ValueError:  
                print('Decoding JSON has failed')
            except json.decoder.JSONDecodeError:
            	print("String could not be converted to JSON")

        print()
        print('-----------------END-----------------')
        return 1
       

    




"""
Entry point
"""
main = Main()
main.run()

