from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType

from app.api.queries import listCaptions_resolver, getCaption_resolver, relatedCaptions_resolver, get_newfeed, \
    getAuthor_resolver
from app.api.mutations import add_caption_resolver, update_user_resolver

query = ObjectType("Query")
query.set_field("listCaptions", listCaptions_resolver)
query.set_field("getCaption", getCaption_resolver)
query.set_field("relatedCaptions", relatedCaptions_resolver)
query.set_field("getNewFeed", get_newfeed)
query.set_field("userDetail", getAuthor_resolver)

mutation = ObjectType("Mutation")
mutation.set_field("addCaption", add_caption_resolver)
mutation.set_field("updateUser", update_user_resolver)


type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query, mutation, snake_case_fallback_resolvers
)