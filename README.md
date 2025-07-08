- Workflow:
    - kafka consumer
        - Read the message
        - Get the name and the value
            - Get before, as well as the timestamp
            - Standarize the name
            - Insert it into the in-memory database (List data structure): Function in core (lpush + ltrim)
            - Re-check logic: before & after
            - If change occured:
                - Recompute the service status. 
                - If the current status != the previous status 
                    - Add the status to the history 
                    - In case the change occured from "DOWN" to another status:
                        - Cumulate the downtime sum (computation must be based on the timestap of the event)
    - Commit the message.

---
- The conditions are like, .... check the triggers, but basically 
    - Function(host, item name, history=1) # default value is 1
        - Get from redis the latest "history" values.
        - Do the logic. depending on the function avg, last, max.
            - max of the three latest values is zero

---
- In memroy database: 
    - items:{itemid}   // could be replaced by items:{host}:{itemid}
    - status:{service}
    - downtime:{service}


---  
AOF not available in dragonflydb:
    - start with redis and then switch when the feature is available 
        - 
    - 

---
- Work with itemid:
    - itemid ==> An item in a host (unique)
        - How to get it:
            - from mysql database using a vue ... 

SELECT items.itemid, items.name, hosts.name
    FROM items, hosts
WHERE 
    hosts.hostid = items.hostid
AND
    hosts.name="application"
AND
    items.name="Interface ens192: Inbound packets discarded";

---
- In case adding events: 
    - Publish items and events to the same topic: 
        - Add some checks in order to know whether this is an event or an item, To perform the required logic



--- 
We have two approaches to work: 
    - Each time an item is recieved, rerun everything. 
    - perform some checks



-- TODO: 
    - Integrate with kafka: End to End demo
        - Add stream processing: using faust library, to include only the needed items
    - Add the restapi
    - Think about root cause analytics 



--- 
    - May be some refactoring will be needed
    - Integrating items and events with if else statements and different logics 
        - In case tutor still want to have both, don't forget to isolate this code in a seperate branch
    - Redaction of the readme file
    - push to github 
    - root cause analytics 
    - record an end to end demo 
    - The problem is that dragonflydb doesn't currently support AOF 

--- 
    - Guide 
    - Setup kafka 
        - start and create a topic
    - Setup the kafka reciver tool 
        - just run the command 
    - Start the consumer
    - Start the restapi 


- what if we consume the same messages twice.... since all computations are based on the timestamp of the items, will this really cause a problem ? 



- Test update 