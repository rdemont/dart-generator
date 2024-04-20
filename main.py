import json
from string import Template
import os, stat
import shutil

with open("structure.json") as structFile:
    structFileContent = structFile.read()

structure = json.loads(structFileContent)


shutil.rmtree("results/")
os.makedirs("results/generate/businessObj/")
os.makedirs("results/generate/databaseObj/")
os.makedirs("results/businessObj/")

for table in structure["tables"]:
    for tableName, columns in table.items():
        getFunctions = ""
        setFunctions = ""
        importBusiness = ""
        getColumnName = "  static const String TABLE_NAME = \""+tableName+"\";\n"
        getColumnName += "  static const String COLUMN_ID = \"id\";\n"
        

        variableDefinitionDB = ""
        getFunctionsDB = ""
        setFunctionsDB = ""
        returnVariables = ""
        fromMapVariables = ""
        openfk = ""
        importDB = ""
        cloneDB = ""
                

        for column in columns:
            if (column["ispk"] == "0"):  
            

            
                if(column["type"] == "TEXT"):
                    type = "String"
                    defaultValue = "''"
                    returnVariables += "      "+tableName[0].upper() + tableName[1:]+"Gen.COLUMN_"+column['name'].upper()+" : _"+column['name']+",\n"
                    fromMapVariables += "    _"+column['name']+" = (map["+tableName[0].upper() + tableName[1:]+"Gen.COLUMN_"+column['name'].upper()+"]??'') as "+type+";\n"    
                elif(column["type"] == "INTEGER" or column["type"] == "INT"  ) :
                    type = "int"
                    defaultValue = "0"
                    returnVariables += "      "+tableName[0].upper() + tableName[1:]+"Gen.COLUMN_"+column['name'].upper()+" : _"+column['name']+",\n"
                    fromMapVariables += "    _"+column['name']+" = (map["+tableName[0].upper() + tableName[1:]+"Gen.COLUMN_"+column['name'].upper()+"]??0) as "+type+";\n"    
                    if(column['name'].endswith('Id')) :
                        getFunctions += "  "+column['name'][0:1].upper()+column['name'][1:-2]+" get "+column['name'][0:-2]+" => _localDbObj."+column['name'][0:-2]+";\n"
                        variableDefinitionDB += "  "+column['name'][0:1].upper()+column['name'][1:-2]+" _"+column['name'][0:-2]+" = "+column['name'][0:1].upper()+column['name'][1:-2]+"Gen.newObj();\n"
                        getFunctionsDB += "  "+column['name'][0:1].upper()+column['name'][1:-2]+" get "+column['name'][0:-2]+" => _"+column['name'][0:-2]+";\n"
                        openfk += "        "+column['name'][0:1].upper()+column['name'][1:-2]+"Gen.openObj(_"+column['name']+").then((value){\n"
                        openfk += "          _"+column['name'][0:-2]+" = value ;\n"
                        openfk += "        });\n"
            

                        setFunctions += "  set "+column["name"][0:-2]+"("+column['name'][0:1].upper()+column['name'][1:-2]+" value)\n"
                        setFunctions += "  {\n"
                        setFunctions += "    _localDbObj."+column["name"][0:-2]+" = value;\n"
                        setFunctions += "  }\n"          

                        setFunctionsDB += "  set "+column["name"][0:-2]+"("+column['name'][0:1].upper()+column['name'][1:-2]+" value)\n"
                        setFunctionsDB += "  {\n"
                        setFunctionsDB += "    if (_"+column['name']+" != value.id)\n"
                        setFunctionsDB += "    {\n"
                        setFunctionsDB += "      dataUpdated(); \n"
                        setFunctionsDB += "      _"+column['name']+" = value.id;\n"
                        setFunctionsDB += "      _"+column["name"][0:-2]+" = value;\n"
                        setFunctionsDB += "    }\n"
                        setFunctionsDB += "  }\n"
                        
                        fromMapVariables += "    if (_"+column['name']+" >0 )\n"
                        fromMapVariables += "    {\n"
                        fromMapVariables += "      _"+column['name'][0:-2]+" = await "+column['name'][0:1].upper()+column['name'][1:-2]+"Gen.openObj(_"+column['name']+");\n"
                        fromMapVariables += "    }\n"
                        
                        importDB += "import '../../businessObj/"+column['name'][0:-2]+".dart';\n"
                        importDB += "import '../businessObj/"+column['name'][0:-2]+"Gen.dart';\n"
                        importBusiness += "import '../../businessObj/"+column['name'][0:-2]+".dart';\n"
                        
                elif(column["type"] == "FLOAT"):
                    type = "double"
                    defaultValue = "0.0"
                    returnVariables += "      "+tableName[0].upper() + tableName[1:]+"Gen.COLUMN_"+column['name'].upper()+" : _"+column['name']+",\n"
                    fromMapVariables += "    _"+column['name']+" = (map["+tableName[0].upper() + tableName[1:]+"Gen.COLUMN_"+column['name'].upper()+"]??0.0) as "+type+";\n"                        
                elif(column["type"] == "DATETIME"):
                    type = "DateTime"
                    defaultValue = "DateTime.now()"
                    returnVariables += "      "+tableName[0].upper() + tableName[1:]+"Gen.COLUMN_"+column['name'].upper()+" : _"+column['name']+".millisecondsSinceEpoch,\n"
                    fromMapVariables += "    _"+column['name']+" = DateTime.fromMillisecondsSinceEpoch((map["+tableName[0].upper() + tableName[1:]+"Gen.COLUMN_"+column['name'].upper()+"]??0) as int);\n"
                elif(column["type"] == "BOOLEAN"):
                    type = "bool"
                    defaultValue = "true"
                    returnVariables += "      "+tableName[0].upper() + tableName[1:]+"Gen.COLUMN_"+column['name'].upper()+" : _"+column['name']+",\n"
                    fromMapVariables += "    _"+column['name']+" = ((map["+tableName[0].upper() + tableName[1:]+"Gen.COLUMN_"+column['name'].upper()+"]??0) as int) == 1;\n"    



                getFunctions += f"  {type} get {column['name']} => _localDbObj.{column['name']};\n"


                if(not column['name'].endswith('Id')): 
                    setFunctions += "  set "+column["name"]+"("+type+" value)\n"
                    setFunctions += "  {\n"
                    setFunctions += "    _localDbObj."+column["name"]+" = value;\n"
                    setFunctions += "  }\n"

                    setFunctionsDB += "  set "+column['name']+"("+type+" value)\n"
                    setFunctionsDB += "  {\n"
                    setFunctionsDB += "    if (_"+column['name']+" != value)\n"
                    setFunctionsDB += "    {\n"
                    setFunctionsDB += "      dataUpdated(); \n"
                    setFunctionsDB += "      _"+column['name']+" = value;\n"
                    setFunctionsDB += "    }\n"
                    setFunctionsDB += "  }\n"

                

                variableDefinitionDB += "  "+type+" _"+column['name']+" = "+defaultValue+";\n"
                getFunctionsDB += "  "+type+" get "+column['name']+" => _"+column['name']+";\n"
                
               
                getColumnName += "  static const String COLUMN_"+column['name'].upper()+" = \""+column['name']+"\";\n"


                cloneDB += "    (value as "+tableName[0].upper() + tableName[1:]+"DBGen)._"+column['name']+" = "+column['name']+";\n"
                

        
        values = {
            "tablename": tableName,
            "Tablename": tableName[0].upper() + tableName[1:],
            "getFunctions": getFunctions,
            "setFunctions": setFunctions,
            "importBusiness":importBusiness,
            "getColumnName" : getColumnName,
            
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
            "importDB" : importDB,
            "cloneDB" : cloneDB
        }
        


        with open('tablenameGen.txt', 'r') as f:
            src = Template(f.read())
            result = src.substitute(values)
            print(result)
            
            with open("results/generate/businessObj/" + tableName + "Gen.dart", "w") as dartFile:
                dartFile.write(result)

        with open('tablenameListGen.txt', 'r') as f:
            src = Template(f.read())
            result = src.substitute(values)
            print(result)
            
            with open("results/generate/businessObj/" + tableName + "ListGen.dart", "w") as dartFile:
                dartFile.write(result)


        with open('tablename.txt', 'r') as f:
            src = Template(f.read())
            result = src.substitute(values)
            print(result)
            
            with open("results/businessObj/" + tableName + ".dart", "w") as dartFile:
                dartFile.write(result)

        with open('tablenameList.txt', 'r') as f:
            src = Template(f.read())
            result = src.substitute(values)
            print(result)
            
            with open("results/businessObj/" + tableName + "List.dart", "w") as dartFile:
                dartFile.write(result)

        
        
        with open('tablenameDB.txt', 'r') as f:
            src = Template(f.read())
            result = src.substitute(valuesDB)
            print(result)
            
            with open("results/generate/databaseObj/" + tableName + "DBGen.dart", "w") as dartFile:
                dartFile.write(result)



