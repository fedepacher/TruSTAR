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
        prop_index, prop = issubprop_array(prop)                    #get array index in case property has array characteristics and remove [] from prop str, None if not exist
        result_bool, r = valueexist(r, prop, prop_index)            #get a tuple, r = new list inside list where prop was found if result_bool = true, else prop was not found
        if not result_bool:                                         #false in case not a property in the properties tree
            break
    
    if result_bool:        
        values = get_value(r, array, prop)                          #get array of property´s value
        if not (prop_index is None):                                #if prop_index is != None means tree array
            if len(values) > 0:
                values = [(values[0][prop_index])]                  #find property in the tree array
            else:                                                   
                values = [r]                                        #if len(values) = 0 means no match in get_value function but as result_bool was true prop exist so value is r stored as a list    
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
param prop_index :      index of list       
return result :         true if exist1
return obj_list :       list where was found
"""
def valueexist(obj_list, key, prop_index):
    result = False
    
    if isinstance(obj_list, (dict)):
        for k, v in obj_list.items():
            if k == key:
                result = True
                if isinstance(v, (dict)):
                    obj_list = v
                elif not (prop_index is None) and isinstance(v, (list)):
                    if len(v) <= prop_index:
                        result = False
                    else:
                        obj_list = v
                break      
    elif isinstance(obj_list, (list)):
        for item in obj_list:
            if item == key:
                result = True
            elif isinstance(item, (dict)):
                result, aux = valueexist(item, key, prop_index)

    return result, obj_list

"""
Convert properties in an array of properties, if "." exist mean a sub prop inside prop
param properties :       str of properties separated with "."    
return prop_array :      array of properties
"""
def issubprop(properties):
    prop_array = properties.split(".")   
    return prop_array


"""
Get index of array in case exist
param properties :      str of properties separated with "."   
return index_array:     index of array in case existe, None if not
return prop_array :     property without "[xx]"
"""
def issubprop_array(property):
    start_index_par1 = property.find('[')                                       #get '[' index in string
    end_index_par2 = property.find(']')                                         #get ']' index in string
    prop_aux = property
    if start_index_par1 != -1 and end_index_par2 != -1:                         #if no char ret value -1
        prop_aux = str(property)[ 0 : start_index_par1 : ]                      #get substring without parentesis                     
        start_index_par1 = start_index_par1 + 1                                 #add 1 to get number index
        index_array = int(str(property)[start_index_par1: end_index_par2: abs(end_index_par2 - start_index_par1)])  #get index
    else:
        index_array = None                                                      #if no index array set as None 
    return index_array, prop_aux