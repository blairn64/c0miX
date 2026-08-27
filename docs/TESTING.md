# Testing Strategy

The application uses pytest with an isolated temporary SQLite database so tests do not depend on a developer's local collection.

## Current coverage

- Creating a series through the HTTP layer
- Returning collection summaries through the API
- Missing-issue calculation
- Excluding reprints from canonical missing-issue results

## Next tests

- Duplicate series and issue handling
- Invalid issue numbers
- Ownership/read-state updates
- Variant ordering
- Series deletion and foreign-key cleanup
- API error responses

The test suite should stay focused on externally visible behaviour and the core collection domain rules.
