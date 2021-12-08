from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType

from app.api.queries import listCaptions_resolver, getCaption_resolver

query = ObjectType("Query")
query.set_field("listCaptions", listCaptions_resolver)
query.set_field("getCaption", getCaption_resolver)

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query, snake_case_fallback_resolvers
)