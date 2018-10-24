- endpoint/service/repository/model -
- No Error Handling
- Class person should inherit from object - https://stackoverflow.com/a/45062077/5019818
- Class person constructor id shadows built-in function id.
- Class person constructor first_name typo.
- Class person constructor What if addresses/family_members are None?
- In /people - no data validation, also POST can override existing data if '_id' exists
- Repeating code of Mongo client
- KeyError if MONGO_HOST or MONGO_PORT do not exist
- When listing all should list minimum information - and not whole objects
- When filtering in REST should be done via query parameters and not path params
- In /people/last_name/<last_name> - c/p error using first_name
- In /people/<id> - When updating existing should use PUT instead of POST
- In /people/<id> - Updating family members and addresses is gruesome code. Should be handled in service/model layer.
  (Depending if you want immutable objects or not)
- No Tests - Of curse in the current state of the code it is very hard to check it. If changed to service, repository,
  model, each can be tested easier by mocking usually one call to the next layer.