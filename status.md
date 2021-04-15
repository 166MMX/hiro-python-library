## Packages

| package          | comment      |
|------------------|--------------|
| arago.ontology   |              |
| arago.ogit       | generated    |
| arago.hiro_sdk   | frontend abc |
| arago.hiro_rest  | backend impl |
| arago.hiro_data  | backend impl |
| arago.hiro_model | backend impl |

## Actions

| api      |                  | action  | frontend rest | frontend data | frontend model | 5 rest | 5 data | 5 model | 6 rest | 6 data | 6 model | 7 rest | 7 data | 7 model | comment  |
|----------|------------------|---------|:-------------:|:-------------:|:--------------:|:------:|:------:|:-------:|:------:|:------:|:-------:|:------:|:------:|:-------:|----------|
| meta     | info             |         |               |               |                |        |        |         | x      | x      | x       | n/a    | n/a    | n/a     |          |
| meta     | version          |         |               |               |                | n/a    |        |         | n/a    | static | x       | x      | x      | x       |          |
| meta     | versions         |         |               |               |                | n/a    |        |         | n/a    | static | x       | x      | x      | x       |          |
| health   | health           | check   |               |               |                |        |        |         | x      | x      | x       |        |        |         |          |             
| auth     | token            | get     |               |               |                |        |        |         | x      | x      | x       |        |        |         |          |
| auth     | token            | refresh |               |               |                |        |        |         | n/a    | n/a    | n/a     |        |        |         |          |
| auth     | token            | revoke  |               |               |                |        |        |         | x      | x      | x       |        |        |         |          |
| graph    | edge             | create  |               |               |                |        |        |         | x      | x      | x       | x      | x      |         |          |
| graph    | edge             | delete  |               |               |                |        |        |         | x      | x      | x       | x      | x      |         |          |
| graph    | vertex           | create  |               |               |                |        |        |         | x      | x      | x       | x      | x      |         |          |
| graph    | vertex           | get     |               |               |                |        |        |         | x      | x      | x       | x      | x      |         |          |
| graph    | vertex           | update  |               |               |                |        |        |         | x      | x      | x       | x      | x      |         |          |
| graph    | vertex           | delete  |               |               |                |        |        |         | x      | x      | x       | x      | x      |         |          |
| graph    | vertex           | history |               |               |                |        |        |         | x      | x      | x       | x      | x      |         |          |
| graph    | events           | ...     |               |               |                |        |        |         |        |        |         |        |        |         |          |
| search   | index            |         |               |               |                |        |        |         | x      | x      | x       | x      | x      |         |          |
| search   | graph            |         |               |               |                |        |        |         | x      | x      | x       | x      | x      |         |          |
| storage  | blob             | set     |               |               |                |        |        |         | x      | x      | x       |        |        |         |          |
| storage  | blob             | get     |               |               |                |        |        |         | x      | x      | x       |        |        |         |          |
| storage  | log              | ...     |               |               |                |        |        |         |        |        |         |        |        |         |          |
| storage  | time series      | add     |               |               |                |        |        |         | x      | x      | x       |        |        |         |          |
| storage  | time series      | get     |               |               |                |        |        |         | x      | x      | x       |        |        |         |          |
| app      | ...              | ...     |               |               |                |        |        |         |        |        |         |        |        |         |          |
| iam      | application      | ...     |               |               |                |        |        |         |        |        |         |        |        |         |          |
| iam      | account          | ...     |               |               |                |        |        |         |        |        |         |        |        |         |          |
| iam      | role             | ...     |               |               |                |        |        |         |        |        |         |        |        |         |          |
| iam      | scope            | ...     |               |               |                |        |        |         |        |        |         |        |        |         |          |
| iam      | organization     | ...     |               |               |                |        |        |         |        |        |         |        |        |         |          |
| iam      | domain           | ...     |               |               |                |        |        |         |        |        |         |        |        |         |          |
| iam      | team             | ...     |               |               |                |        |        |         |        |        |         |        |        |         |          |
| iam      | data set         | ...     |               |               |                |        |        |         |        |        |         |        |        |         |          |
| mars     | machine          | ...     |               |               |                |        |        |         |        |        |         |        |        |         |          |
| mars     | application      | ...     |               |               |                |        |        |         |        |        |         |        |        |         |          |
| mars     | resource         | ...     |               |               |                |        |        |         |        |        |         |        |        |         |          |
| mars     | software         | ...     |               |               |                |        |        |         |        |        |         |        |        |         |          |
| engine   | automation issue | ...     |               |               |                |        |        |         |        |        |         |        |        |         |          |
| engine   | knowledge item   | ...     |               |               |                |        |        |         |        |        |         |        |        |         |          |
| engine   | knowledge pool   | ...     |               |               |                |        |        |         |        |        |         |        |        |         |          |
| engine   | variable         | ...     |               |               |                |        |        |         |        |        |         |        |        |         |          |
| ...      | calender         | ...     |               |               |                |        |        |         |        |        |         |        |        |         |          |
| do       | view             | ...     |               |               |                |        |        |         |        |        |         |        |        |         |          |
| do       | object           | ...     |               |               |                |        |        |         |        |        |         |        |        |         |          |

## Models

| api      | ogit                            | py                                      |  5  |  6  |  7  |
|----------|---------------------------------|-----------------------------------------|:---:|:---:|:---:|
| ontology | ogit:Entity                     | arago.hiro.model.ontology.Entity        |     |     |     |
| ontology | ogit:Verb                       | arago.hiro.model.ontology.Verb          |     |     |     |
| ontology | ogit:Attribute                  | arago.hiro.model.ontology.Attribute     |     |     |     |
| ontology | n/a                             | arago.hiro.model.ontology.Namespace     |     |     |     |
| ogit     | ogit:OntologyEntity             | arago.hiro.model.ogit.Entity            |     |     |     |
| ogit     | ogit:OntologyVerb               | arago.hiro.model.ogit.Verb              |     |     |     |
| ogit     | ogit:OntologyAttribute          | arago.hiro.model.ogit.Attribute         |     |     |     |
| ogit     | n/a                             | arago.hiro.model.ogit.Namespace         |     |     |     |
| meta     | n/a                             | arago.hiro.model.Api                    | -   | -   | x   |
| meta     | n/a                             | arago.hiro.backend.Version              | x   | x   | x   |
| auth     | n/a                             | arago.hiro.model.AccessToken            |     | x   | x   |
| graph    | n/a                             | arago.hiro.model.graph.Vertex           |     | x   | x   |
| graph    | n/a                             | arago.hiro.model.graph.VertexId         |     | x   | x   |
| graph    | n/a                             | arago.hiro.model.graph.ExternalVertexId | -   | x   | x   |
| graph    | n/a                             | .VertexHistory                          |     |     |     |
| graph    | n/a                             | arago.hiro.model.graph.Edge             |     |     |     |
| graph    | n/a                             | arago.hiro.model.graph.EdgeId           |     |     |     |
| storage  | ogit:Attachment                 | .Blob                                   |  o  |  x  |  o  |
| storage  | n/a                             | arago.hiro.model.graph.BlobId           |     |     |     |
| storage  | ogit.Data:Log                   | .Log                                    |  -  |  o  |  -  |
| storage  | n/a                             | arago.hiro.model.graph.LogId            |     |     |     |
| storage  | ogit:Timeseries                 | .TimeSeries                             |  o  |  x  |  o  |
| storage  | n/a                             | arago.hiro.model.graph.TimeSeriesId     |     |     |     |
| storage  | n/a                             | .TimeSeriesValue                        |     |     |     |
| app      | ...                             | ...                                     |     |     |     |
| iam      | ogit.Auth:Account               | .Account                                |  -  |  o  |  o  |
| iam      | ogit.Auth:Application           | .Application                            |  -  |  o  |  o  |
| iam      | ogit.Auth:Role                  | .Role                                   |  -  |  o  |  o  |
| iam      | ogit.Auth:DataScope             | .Scope                                  |  -  |  -  |  o  |
| iam      | ogit.Auth:Organization          | .Organization                           |  -  |  -  |  o  |
| iam      | ogit.Auth:OrgDomain             | .Domain                                 |  -  |  -  |  o  |
| iam      | ogit.Auth:Team                  | .Team                                   |  -  |  -  |  o  |
| iam      | ogit.Auth:DataSet               | .DataSet                                |  -  |  -  |  o  |
| mars     | ogit.MARS:Machine               | .Machine                                |  o  |  o  |  o  |
| mars     | ogit.MARS:Application           | .Application                            |  o  |  o  |  o  |
| mars     | ogit.MARS:Resource              | .Resource                               |  o  |  o  |  o  |
| mars     | ogit.MARS:Software              | .Software                               |  o  |  o  |  o  |
| engine   | ogit.Automation:AutomationIssue | .AutomationIssue                        |  o  |  o  |  o  |
| engine   | n/a                             | .AutomationIssueHistory                 |     |     |     |
| engine   | ogit.Automation:KnowledgeItem   | .KnowledgeItem                          |  o  |  o  |  o  |
| engine   | ogit.Automation:KnowledgePool   | .KnowledgePool                          |  o  |  o  |  o  |
| engine   | ogit.Automation:Variable        | .Variable                               |  o  |  o  |  o  |
| engine   | ogit:LicenseRequest             |                                         |  o  |  o  |  o  |
| ...      | ogit.Schedule:Calendar          | .Calender                               |  o  |  o  |  o  |
