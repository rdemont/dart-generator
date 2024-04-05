import json
from string import Template
import os, stat
import shutil

with open("structure.json") as structFile:
    structFileContent = structFile.read()

structure = json.loads(structFileContent)


shutil.rmtree("results/")
os.makedirs("results/businessObj/gen/")
os.makedirs("results/databaseObj/")

for table in structure["tables"]:
    for tableName, columns in table.items():
        getFunctions = ""
        setFunctions = ""
        importBusiness = ""

        variableDefinitionDB = ""
        getFunctionsDB = ""
        setFunctionsDB = ""
        returnVariables = ""
        fromMapVariables = ""
        openfk = ""
        importDB = ""

        for column in columns:
            if (column["ispk"] == "0"):  
            

            
                if(column["type"] == "TEXT"):
                    type = "String"
                    defaultValue = "''"
                    returnVariables += "      '"+column['name']+"' : _"+column['name']+",\n"
                    fromMapVariables += "    _"+column['name']+" = (map['"+column['name']+"']??'') as "+type+";\n"    
                elif(column["type"] == "INTEGER" or column["type"] == "INT"  ) :
                    type = "int"
                    defaultValue = "0"
                    returnVariables += "      '"+column['name']+"' : _"+column['name']+",\n"
                    fromMapVariables += "    _"+column['name']+" = (map['"+column['name']+"']??0) as "+type+";\n"    
                    if(column['name'].endswith('Id')) :
                        getFunctions += "  "+column['name'][0:1].upper()+column['name'][1:-2]+" get "+column['name'][0:-2]+" => _localDbObj."+column['name'][0:-2]+";\n"
                        variableDefinitionDB += "  "+column['name'][0:1].upper()+column['name'][1:-2]+" _"+column['name'][0:-2]+" = "+column['name'][0:1].upper()+column['name'][1:-2]+"Impl.newObj();\n"
                        getFunctionsDB += "  "+column['name'][0:1].upper()+column['name'][1:-2]+" get "+column['name'][0:-2]+" => _"+column['name'][0:-2]+";\n"
                        openfk += "        "+column['name'][0:1].upper()+column['name'][1:-2]+"Impl.openObj(_"+column['name']+").then((value){\n"
                        openfk += "          _"+column['name'][0:-2]+" = value ;\n"
                        openfk += "        });\n"
            
                        
                        fromMapVariables += "    if (_"+column['name']+" >0 )\n"
                        fromMapVariables += "    {\n"
                        fromMapVariables += "      _"+column['name'][0:-2]+" = await "+column['name'][0:1].upper()+column['name'][1:-2]+"Impl.openObj(_"+column['name']+");\n"
                        fromMapVariables += "    }\n"
                        
                        importDB += "import '../businessObj/"+column['name'][0:-2]+".dart';\n"
                        importDB += "import '../businessObj/gen/"+column['name'][0:-2]+"Impl.dart';\n"
                        importBusiness += "import '../"+column['name'][0:-2]+".dart';\n"
                        
                elif(column["type"] == "FLOAT"):
                    type = "double"
                    defaultValue = "0.0"
                    returnVariables += "      '"+column['name']+"' : _"+column['name']+",\n"
                    fromMapVariables += "    _"+column['name']+" = (map['"+column['name']+"']??0.0) as "+type+";\n"                        
                elif(column["type"] == "DATETIME"):
                    type = "DateTime"
                    defaultValue = "DateTime.now()"
                    returnVariables += "      '"+column['name']+"' : _"+column['name']+".millisecondsSinceEpoch,\n"
                    fromMapVariables += "    _"+column['name']+" = DateTime.fromMillisecondsSinceEpoch((map['"+column['name']+"']??0) as int);\n"
                elif(column["type"] == "BOOLEAN"):
                    type = "bool"
                    defaultValue = "true"
                    returnVariables += "      '"+column['name']+"' : _"+column['name']+",\n"
                    fromMapVariables += "    _"+column['name']+" = ((map['"+column['name']+"']??0) as int) == 1;\n"    


                getFunctions += f"  {type} get {column['name']} => _localDbObj.{column['name']};\n"
                setFunctions += "  set "+column["name"]+"("+type+" value)\n"
                setFunctions += "  {\n"
                setFunctions += "    _localDbObj."+column["name"]+" = value;\n"
                setFunctions += "  }\n"
                

                variableDefinitionDB += "  "+type+" _"+column['name']+" = "+defaultValue+";\n"
                getFunctionsDB += "  "+type+" get "+column['name']+" => _"+column['name']+";\n"
                setFunctionsDB += "  set "+column['name']+"("+type+" value)\n"
                setFunctionsDB += "  {\n"
                setFunctionsDB += "    if (_"+column['name']+" != value)\n"
                setFunctionsDB += "    {\n"
                setFunctionsDB += "      dataUpdated(); \n"
                setFunctionsDB += "      _"+column['name']+" = value;\n"
                setFunctionsDB += "    }\n"
                setFunctionsDB += "  }\n"
                
               

        
        values = {
            "tablename": tableName,
            "Tablename": tableName[0].upper() + tableName[1:],
            "getFunctions": getFunctions,
            "setFunctions": setFunctions,
            "importBusiness":importBusiness
        }

        valuesDB = {
            "variableDefinition": variableDefinitionDB,
            "tablename": tableName,
            "Tablename": tableName[0].upper() + tableName[1:],
            "getFunctions": getFunctionsDB,
            "setFunctions": setFunctionsDB,
            "returnVariables": returnVariables,
            "fromMapVariables": fromMapVariables,
            "openfk": openfk,
            "importDB" : importDB
        }
        


        with open('tablenameImpl.txt', 'r') as f:
            src = Template(f.read())
            result = src.substitute(values)
            print(result)
            
            with open("results/businessObj/gen/" + tableName + "Impl.dart", "w") as dartFile:
                dartFile.write(result)

        with open('tablename.txt', 'r') as f:
            src = Template(f.read())
            result = src.substitute(values)
            print(result)
            
            with open("results/businessObj/" + tableName + ".dart", "w") as dartFile:
                dartFile.write(result)

        
        with open('tablenameDB.txt', 'r') as f:
            src = Template(f.read())
            result = src.substitute(valuesDB)
            print(result)
            
            with open("results/databaseObj/" + tableName + "DB.dart", "w") as dartFile:
                dartFile.write(result)



