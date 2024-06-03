# 
# A stand-alone script capable of reading a nosj formatted input 
# file passed through the command line and print to standard output.
#
#
# Joshua Wyatt - 
#
from operator import index
import sys
from os.path import isfile
import urllib.parse

class nosjReader :
    mapTracker = 0 #notes how many maps are founded *Swap for RE
    value = ""
    key = ""
    mode = 0
    keyNames  = []
    valueNames = []
    valAndType = []
    if isfile(sys.argv[1]) :
        with open(sys.argv[1], 'r') as file :
            contain = file.read()
            contain = contain.strip() # removes leading and trailing whitespace

            # Added in patch
            if not contain :
                sys.stderr.write("ERROR -- File is empty")
                sys.exit(66) 
            # End of patched content
            if contain[0] != "<" : # Checks if map begins with '<'
                sys.stderr.write("ERROR -- Should begin with '<'")
                sys.exit(66) 


            #greatTracker = greatTracker + 1
            for c in contain:
                if mode == 0 : 
                    if c == "<" :
                        if mapTracker > 0 :
                            valueNames.append(None)
                        mapTracker += 1
                        mode = 1
                    else :
                        mode = 2
                # Sorting out key 
                elif mode == 1 :
                    if c == ">" :
                        # Added in patch
                        if key :
                            sys.stderr.write("ERROR -- Key is missing its ':' and value")
                            sys.exit(66) 
                            #end of patched content      
                        mode = 3
                    elif c != ":" :
                        key = key + c
                    elif c == ":" :
                        if (key,mapTracker) in keyNames :
                            sys.stderr.write("ERROR -- Key is not unique to this map")
                            sys.exit(66) 
                        
                        # Added in patch
                        if key == "" :
                            sys.stderr.write("ERROR -- Empty Key")
                            sys.exit(66)  
                            #end of update
                        elif key.isalnum() :
                            keyNames.append((key,mapTracker))  
                            key = ""
                        else :
                            sys.stderr.write("ERROR -- Key is not alphanumeric")
                            sys.exit(66) 
                        mode = 0
                
                # Value Brand
                if mode == 2 :
                    if c == ">" :
                        # Added in patch
                        if not value :
                            sys.stderr.write("ERROR -- Empty Value for key")
                            sys.exit(66) 
                            # End of patched content
                        if value[0] == " " or value[-1] == " " :
                            sys.stderr.write("ERROR -- Whitespace was found before or after the value, which is not allowed")
                            sys.exit(66) 
                        mode = 3
                        valueNames.append(value)
                        value = ""
                    elif c == "," :
                        if value[0] == " " or value[-1] == " " :
                            sys.stderr.write("ERROR -- Whitespace was found before or after the value, which is not allowed")
                            sys.exit(66) 
                        valueNames.append(value)
                        value = ""
                        mode = 1
                    else :
                        value = value + c
                        
                # Checking end 
                if mode == 3 :
                    if c == ">" :
                        mapTracker -= 1
                    elif c == "," :
                        mode = 1
                    else :
                        sys.stderr.write("ERROR -- There appears to be characters after the final '>', which is not allowed")
                        sys.exit(66) 
            if mapTracker != 0 :
                sys.stderr.write("ERROR -- There is an imbalance of '<' and '>' symbols")
                sys.exit(66) 



        # Identifying Types Values
        for val in valueNames :

            # Checks for map type
            if val is None :
                valAndType.append(("","(map)"))
            # Checks for complex strings
            elif "%" in val :
                testValue = val.replace("%","")
                if testValue.isalnum() == False :
                    sys.stderr.write("ERROR -- Value does not fulfil requirements for a complex string and does not fit the other types")
                    sys.exit(66)
                val = (urllib.parse.unquote(val), "(string)")
                valAndType.append(val)
            # Checks for simple strings
            elif val[-1] == "s" :
                testValue = val.replace(" ","")
                if testValue.isalnum() == False :
                    sys.stderr.write("ERROR -- Value does not fulfil requirements for simple string and does not fit the other types")
                    sys.exit(66)
                valAndType.append((val[:-1], "(string)"))
            # checks for integers
            elif val[0] == "i" :
                testValue = val
                if val[1] == "-" :
                    testValue = val[:1] + val[2:]
                if testValue.isalnum() == False :
                    sys.stderr.write("ERROR -- Value does not fulfil requirements for integer and does not fit the other types")
                    sys.exit(66)
                valAndType.append((val[1:],"(integer)"))
            else :
                sys.stderr.write("ERROR -- Value is of an invalid type")
                sys.exit(66)
            testValue = ""
       
        previousK = 1
        count = 0
        mpcount = 0
        sys.stdout.write("begin-map\n")
        for k in keyNames :
            if previousK < k[1] :
                sys.stdout.write("begin-map\n")
                mpcount += 1
            sys.stdout.write(k[0] + " -- " + valAndType[count][1] + " -- " + valAndType[count][0] + "\n")
            if previousK > k[1] :
                sys.stdout.write("end-map\n")
                mpcount -= 1
            previousK = k[1]
            count += 1
        for n in range(mpcount)  :
            sys.stdout.write("end-map\n")
        sys.stdout.write("end-map")
        # Printing out data 
        # valAndType and keyNames
            
                
    else :
        sys.stderr.write("ERROR -- invalid file path, please input a valid pathway and try again")
        sys.exit(66)
    