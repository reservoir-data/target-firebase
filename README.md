# target-firebase

`target-firebase` is a Singer target for Firebase.

Build with the [Meltano Target SDK](https://sdk.meltano.com).

## Installation

Install from PyPI:

```bash
uv tool install target-firebase
```

Install from GitHub:

```bash
uv tool install git+https://github.com/ORG_NAME/target-firebase.git@main
```

## Configuration

### Accepted Config Options
| Setting | Required | Default | Description |
|:--------|:--------:|:-------:|:------------|
| credential_file | False | None | The path to the Google Cloud Firestore credential file. If none is provided, Google Application Default Credentials are used. |
| credential | False | None | The Google Cloud Firestore credential object. If none is provided, Google Application Default Credentials are used. |
| credential.type | True | service_account | The type of credential. |
| credential.client_email | True | None | The service account's email. |
| credential.token_uri | False | https://oauth2.googleapis.com/token | The OAuth 2.0 Token URI. |
| credential.project_id | True | None | Project ID associated with the service account credential. |
| credential.universe_domain | False | None | The universe domain. The default universe domain is googleapis.com. For default value self signed jwt is used for token refresh. |
| credential.trust_boundary | False | None | String representation of trust boundary meta. |
| firebase_app | False | [DEFAULT] | The name of the Firebase app to use. |
| database_id | False | None | The database ID of the Google Cloud Firestore database to be used. Defaults to the default Firestore database ID if not specified or an empty string. |
| add_record_metadata | False | None | Whether to add metadata fields to records. |
| load_method | False | TargetLoadMethods.APPEND_ONLY | The method to use when loading data into the destination. `append-only` will always write all input records whether that records already exists or not. `upsert` will update existing records and insert new records. `overwrite` will delete all existing records and insert all input records. |
| batch_size_rows | False | None | Maximum number of rows in each batch. |
| validate_records | False | True | Whether to validate the schema of the incoming streams. |
| stream_maps | False | None | Config object for stream maps capability. For more information check out [Stream Maps](https://sdk.meltano.com/en/latest/stream_maps.html). |
| stream_maps.__else__ | False | None | Currently, only setting this to `__NULL__` is supported. This will remove all other streams. |
| stream_map_config | False | None | User-defined config values to be used within map expressions. |
| faker_config | False | None | Config for the [`Faker`](https://faker.readthedocs.io/en/master/) instance variable `fake` used within map expressions. Only applicable if the plugin specifies `faker` as an additional dependency (through the `singer-sdk` `faker` extra or directly). |
| faker_config.seed | False | None | Value to seed the Faker generator for deterministic output: https://faker.readthedocs.io/en/master/#seeding-the-generator |
| faker_config.locale | False | None | One or more LCID locale strings to produce localized output for: https://faker.readthedocs.io/en/master/#localization |
| flattening_enabled | False | None | 'True' to enable schema flattening and automatically expand nested properties. |
| flattening_max_depth | False | None | The max depth to flatten schemas. |

A full list of supported settings and capabilities for this
target is available by running:

```bash
target-firebase --about
```

### Configure using environment variables

This Singer target will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

## Usage

You can easily run `target-firebase` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Target Directly

```bash
target-firebase --version
target-firebase --help
# Test using the "Smoke Test" tap:
tap-smoke-test | target-firebase --config /path/to/target-firebase-config.json
```

## Developer Resources

Follow these instructions to contribute to this project.

### Initialize your Development Environment

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh  # or see https://docs.astral.sh/uv/getting-started/installation/
uv sync
```

### Create and Run Tests

Create tests within the `tests` subfolder and
  then run:

```bash
uv run pytest
```

You can also test the `target-firebase` CLI interface directly using `uv run`:

```bash
uv run target-firebase --help
```

### Testing with [Meltano](https://meltano.com/)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Use Meltano to run an EL pipeline:

```bash
# Test invocation:
uvx meltano invoke tap-firebase --version

# OR run a test `elt` pipeline:
uvx meltano run tap-firebase target-jsonl
```
### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the Meltano Singer SDK to
develop your own Singer taps and targets.
