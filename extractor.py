"""
Find values from nested JSON in case exist.
param obj_list :    JSON list
param key :         value to be searched    
return array :      array of found elementets, empty if not find it 
"""
def json_interpreter(obj_list, key):
    array = []
    values = []
    prop_array = issubprop(key)
    r = obj_list                                        #save obj_list
    for prop in prop_array:
        result_bool, r = valueexist(r, prop)            #get a tuple, r = new list inside list where prop was found if result_bool = true, else prop was not found
        if not result_bool:
            break
    
    if result_bool:        
        values = get_value(r, array, prop)#key)
    return values

"""
Search values recursively from nested JSON in case exist.
param obj_list :    JSON list
param array :       array of found elements
param key :         value to be searched    
return array :      array of found elementets, empty if not find it 
"""
def get_value(obj_list, array, key):
    if isinstance(obj_list, dict):
        for k, v in obj_list.items():
            if  k == key:
                array.append(v)
            elif isinstance(v, (dict, list)):
                get_value(v, array, key)
    elif isinstance(obj_list, list):
        for item in obj_list:
            get_value(item, array, key)
    return array

"""
Search if property exists, if exists return true and the list where was found
param obj_list :        JSON list 
param key :             value to be searched     
return result :         true if exist1
return obj_list :       list where was found
"""
def valueexist(obj_list, key):
    result = False
    
    if isinstance(obj_list, dict):
        for k, v in obj_list.items():
            if k == key:
                result = True
                if isinstance(v, (dict)):
                    obj_list = v
                break      

    return result, obj_list

"""
Convert properties in an array of properties, if "." exist mean a sub prop inside prop
param properties :       str of properties separated with "."    
return prop_array :      array of properties
"""
def issubprop(properties):
    prop_array = properties.split(".")   
    return prop_array