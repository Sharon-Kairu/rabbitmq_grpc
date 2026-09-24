import graphene
import provider.schema

class Query(provider.schema.Query, graphene.ObjectType):
    pass

class Mutation(provider.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)