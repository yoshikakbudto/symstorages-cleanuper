# Symbol servers cleanuper

The tool helps to keep cleaner your symbol server storage by utilizing propriatary tools.

The logic is that:
1. Collect symbols metadata in the binary build task and store it in a database.
2. Configure a cleanup policy based on the metadata fields.
2. Apply the cleanup policy to search and delete an unneeded symbols.