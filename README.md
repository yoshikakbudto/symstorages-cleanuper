# Symbol servers cleanuper

The tool helps to keep cleaner your symbol server storage by utilizing propriatary tools.

The logic is that:

1. Collect symbols metadata in the binary build task and store it in a database.
1. Configure a cleanup policy based on the metadata fields.
1. Apply the cleanup policy to search and delete an unneeded symbols.

## Run tests

To run tests execute these commands:

```sh
poetry install
poetry shell
pytest
```

you can filter only specific test by specifying only test name substring with the `-k` parameter: `pytest -k "test_datafile"`

## Build and publish

1. Bump version via `poetry version --help`
1. Build distribution package: `poetry build`
1. Publish: `poetry publish -r targem`
