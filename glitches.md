* gremlin valueMap() exposing ogit/_metadata
* gremlin valueMap() missing ogit/_graphtype
* gremlin valueMap() ogit/_type two values duplicated (e.g. id:'ogit/Node')
* vertex/history DELETE request responds with status code 200 (H6) should be 405
* investigate HistoryFormat.ELEMENT ogit/_v behavior (H6)
* search/external responds with status code 200 should be 404
* boolean (query) parameters only accept case-sensitive 'true' everything else is treated as False
* timeseries/get from/to params require left padded integer strings (H6)
* app/ui/activate responding with old status value (H6)
* help pages refers to /api/version.json and /api/versions.json but replies with 403
* app-admin is listed on help page but not in /api/version or /api/versions #7933 (H7)
* vertex/history undocumented support includeDeleted