from types import SimpleNamespace

HTTP_HEADER_HOST = 'X-FORWARDED-HOST'
HTTP_HEADER_PORT = 'X-FORWARDED-PORT'
HTTP_HEADER_PROTOCOL = 'X-FORWARDED-PROTO'

ENV_CONNECTION_STRING = "MyCosmosDBConnectionString"
HEADER_EMAIL="X-REQUEST-EMAIL"
DB_NAME = "development"
COL_USERS = "users"
COL_SUBMISSIONS = "submissions"
COL_TASKS = "tasks"
COL_CASES = "test_cases"
COL_TESTS = "submitted_tests"

SCHEMA_USER = SimpleNamespace (
    EMAIL="email",
    ROLES="roles",
    IS_ADMIN="is_admin",
)

SCHEMA_TASKS_NAME = "name"
SCHEMA_TASKS_DESCRIPTION = "description"
