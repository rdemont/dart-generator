Generator for flutter/Dart code base on a json with the structure (exemple is file structure.json)



can be made in the openDB with this code and import 'dart:developer';

```
db.rawQuery('SELECT * FROM sqlite_master ORDER BY name;').then((tables) 
    {
      if (tables.length > 0) 
      {
        String strjson = "{\"tables\":[" ; 
        for (int i = 0; i < tables.length; i++) 
        {

          String tableName = tables[i]['name'].toString() ; 
          if ((tableName != "sqlite_sequence") && (tableName != "android_metadata"))
          {
            db.rawQuery("PRAGMA table_info('$tableName')").then((cols)
            {
              db.rawQuery("SELECT count(*) as nb FROM $tableName").then((count)
              {
                  db.rawQuery("SELECT * FROM $tableName ORDER BY ID ").then((raws){
                  print("TABLE : $tableName / NB-Raw : "+count[0]['nb'].toString());          
                  print(tables[i]);
                  for (int iraw = 0 ; iraw<raws.length;iraw++)
                  {
                    print(raws[iraw]);
                  }

                  
                });

              });

              strjson += "{\"$tableName\":[";
              for(int icol = 0;icol < cols.length;icol++)
              {
                String colName = cols[icol]['name'].toString();
                String colType = cols[icol]['type'].toString();
                String colpk = cols[icol]['pk'].toString();
                String colNotnull = cols[icol]['notnull'].toString();
               
                strjson += "{\"name\":\"$colName\",\"type\":\"$colType\",\"ispk\":\"$colpk\",\"notnull\":\"$colNotnull\"},";
              }
              strjson = strjson.substring(0,strjson.length-1)+"]},";


              if (i == tables.length-1)
              {
                strjson = strjson.substring(0,strjson.length-1)+"]}";
                print("*********************JSON STRUCTURE ******************************");
                log(strjson);
                print("*********************END JSON STRUCTURE ******************************");
              }
            });
          }
        }
        
      }
    }
```

