# HIRO Python SDK
This SDK provides:

* Endpoint probes for HIRO 5, HIRO 6 and HIRO 7   
* Backend framework for HIRO 5, HIRO 6 and HIRO 7 implementations
* Frontend framework that passes calls seamlessly to the proper backend implementation
* Layers
    * REST layer that provides low level access for full control
    * Data layer that provides primitive type support
    * Model layer that provides most safety and convenience
* Request and response streaming support based on generators through all layers
* Model objects
    * Ontology (namespace, attribute, entity, verb)
    * Graph (vertex, edge)
    * Storage (time series, blob)
    * OGIT (generated immutable ontology objects) implemented as enum with ontology instances as its values

The main focus is on HIRO 6 and HIRO 7 and end user API. HIRO 5 and admin user API have been considered but prioritised as low priority for now.

## Terminology

* **Ontology**  
Is like a schema or class definition for the graph, it describes how instances or objects will be shaped within the graph.
* **Entity**  
Is like class and is used as a blueprint and validation schema for a vertex instance within a graph.
* **Attribute (entity)**  
Is like a property, field or variable that can be associate with an entity.
* **Verb**  
Is used to describe possible connection types between entities.
* **OGIT**  
Using the basic building blocks of an Ontology. Declaring a concrete entities, attributes and verbs.
* **Vertex**  
Is an instance of an entity within the graph. It can store data or represent something else like a storage location.
* **Attribute (vertex)**  
Is an instance of an entity attribute within the graph.
* **Edge**  
Is an instance of a verb and creating a connection between to vertices. HIRO does not support attributes for edges.
* **Graph**  
The persistent storage location for vertices and edges.
* **Engine**  
Processes automation issues stored within the graph.
* **Variable (engine)**  
Maps to a vertex attributes value, free vertex attribute value or just volatile runtime variable value.
* **Automation Issue**  
a.k.a. Issue or Task

## Goal

* tries to merge
  - python graphit
    - https://github.com/arago/graphit-tool
      - https://github.com/arago/graphit-tool/blob/master/graphit.py#L20
  - python integration tests
    - https://github.com/arago/hiro-integration-tests/blob/master/python/main/pylib
    - https://github.com/arago/hiro-release-management/blob/master/pylib/HIRO
  - java hiro cli
    - https://github.com/arago/hiro-clients/tree/master/java
    - https://github.com/arago/hiro-clients/tree/master/python
    - https://docs.hiro.arago.co/hiro/6.2.0/admin/hiro-cli/overview.html
    - https://docs.hiro.arago.co/hiro/5.4.5/hiro-cli-new/overview.html
    - https://docs.hiro.arago.co/hiro/5.4.5/hiro-cli/overview.html
  - full api support
    - https://pod1159.saasarago.com/_api/index.html
    - https://core.arago.co/help/

## Known issues and limitations

* only HIRO 6 partially supported - no IAM and APP support for now
* does not handle GraphIT HTTP Status Code 888 Transaction rollback
* retry for streaming post requests not yet implemented - api change
* does not implement undocumented features in HIRO 6 like:
  - listMeta
  - includeDeleted
  - order by multiple fields
  - contentType for storage
* does not optionally warn about missing ogit/_owner attribute
* missing escape function for elastic search queries

## Use case

- test ogit ontology against graphit

## Features

* focus on lib rather than cli tool
* focus on end user apis later admin apis
* provide overloaded methods with simulated multi dispatch
* provide redacted HTTP debug messages
* provide HTTP debug messages with curl command
* provide structured API access
* support graphit/engine lists
* support web socket events stream 
* support connectit/doapi 

## API layers

1. version (backend)
    - 5.x low priority
    - 6.x
    - 7.x
1. response (stream)
1. data/content (json/dict)
1. model
    - ontology.Entity (ogit:OntologyEntity)
    - ontology.Verb (ogit:OntologyVerb)
    - ontology.Attribute (ogit:OntologyAttribute)
    - ontology.Namespace
    - graph.Vertex
        - .History
    - graph.Edge
    - engine.AutomationIssue (ogit.Automation:AutomationIssue)
        - .History
        - .max_backoff (https://itautopilot.zendesk.com/agent/tickets/7879)
    - engine.KnowledgeItem (ogit.Automation:KnowledgeItem)
    - engine.KnowledgePool (ogit.Automation:KnowledgePool)
    - engine.Variable (ogit.Automation:Variable)
    - storage.Blob (5,6,7) (ogit:Attachment)
    - storage.Log (6) (ogit:Data:Log)
    - storage.Timeseries (5,6,7) (ogit:Timeseries)
    - mars.Machine (5,6,7) (ogit.MARS:Machine)
    - mars.Application (5,6,7) (ogit.MARS:Application)
    - mars.Resource (5,6,7) (ogit.MARS:Resource)
    - mars.Software (5,6,7) (ogit.MARS:Software)
    - iam.Application (6,7) (ogit.Auth:Application)
    - iam.Account (6,7) (ogit.Auth:Account)
    - iam.Role (6,7) (ogit.Auth:Role)
    - iam.Scope (7)
    - iam.Organization (7)
    - iam.Domain (7)
    - iam.Team (7)
    - iam.DataSet (7)
1. convenience

## Actions

- graph
    - edge
        - create
        - delete
    - vertex
        - create 
        - get
        - update
        - delete
        - history
          
        - attribute (jcli; layer 5)
        - connect (jcli; layer 5)
        - disconnect (jcli; layer 5)
        - connected (layer 5)
    - search
        - ids (layer 5)
        - xid (layer 5)
        - elastic_search
        - gremlin
    - ws (web socket)
        - TODO
- store
    - blob
        - get
        - update
    - log
        - get
        - update
        - delete
    - ts (time series)
        - get
        - update
- mars
    - create (jcli; layer 5)
    - get (jcli; layer 5)
    - update (jcli; layer 5)
    - delete (jcli; layer 5)
    - list (jcli; layer 5)
    - count (jcli; layer 5)
    - dump (jcli; layer 5)
    - connect (jcli; layer 5)
    - disconnect (jcli; layer 5)
- app
    - TODO
- iam
    - TODO
- auth
    - login
    - logout
- engine
    - issue
        - create (jcli; layer 5)
        - get (jcli; layer 5)
        - history (jcli)
        - terminate (jcli; layer 5)
        - status (jcli; layer 5)
        - list (jcli; layer 5)
        - count (jcli; layer 5)
    - knowledge_item
        - create (jcli; layer 5)
        - get (jcli; layer 5)
        - update (jcli; layer 5)
        - delete (jcli; layer 5)
        - validate (jcli)
        - deploy (jcli; layer 5)
        - undeploy (jcli; layer 5)
    - variable
        - TODO
    - calendar
        - TODO

## Python package module and class structure

- arago
    - hiro
        - Client
        - model
            - AccessToken
            - ClientCredentials
            - AccountCredentials
            - SessionCredentials
            - ontology
                - Entity
                - Verb
                - Attribute
                - Namespace
            - graph
                - Vertex
                - Edge
            - engine
                - AutomationIssue
                - KnowledgeItem
                - KnowledgePool
                - Variable
            - storage
                - Blob
                - Log
                - Timeseries
            - mars
                - Machine
                - Application
                - Resource
                - Software
            - iam
                - Application
                - Account
                - Role
                - Scope
                - Organization
                - Domain
                - Team
                - DataSet            
        - backend
            - five
                - Probe
                - http
                    - Graph
                    - Store
                    - MARS
                    - Engine
                    - Auth
                - data
                    - Graph
                    - Store
                    - MARS
                    - Engine
                    - Auth
                - model
                    - Graph
                    - Store
                    - MARS
                    - Engine
                    - Auth
                - convenience
                    - Graph
                    - Store
                    - MARS
                    - Engine
                    - Auth
            - six
                - Probe
                - http
                    - Graph
                    - Engine
                    - IAM
                    - Store
                    - MARS
                    - App
                    - Auth
                - data
                    - Graph
                    - Engine
                    - IAM
                    - Store
                    - MARS
                    - App
                    - Auth
                - model
                    - Graph
                    - Engine
                    - IAM
                    - Store
                    - MARS
                    - App
                    - Auth
                - convenience
                    - Graph
                    - Engine
                    - IAM
                    - Store
                    - MARS
                    - App
                    - Auth
            - seven
                - Probe
                - http
                    - Graph
                    - Store
                    - MARS
                    - Engine
                    - IAM
                    - App
                    - Auth
                - data
                    - Graph
                    - Store
                    - MARS
                    - Engine
                    - IAM
                    - App
                    - Auth
                - model
                    - Graph
                    - Store
                    - MARS
                    - Engine
                    - IAM
                    - App
                    - Auth
                - convenience
                    - Graph
                    - Store
                    - MARS
                    - Engine
                    - IAM
                    - App
                    - Auth


## References
* Ontology
    * https://www.w3.org/TR/owl2-overview/
    * https://www.w3.org/TR/rdf-sparql-query/
    * https://www.w3.org/TR/sparql11-overview/
    * https://www.dublincore.org/specifications/dublin-core/dcmi-terms/
