import graphene
from graphene_django import DjangoObjectType

from graphene_app.models import Category, Ingredient

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "ingredients")


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "notes", "category")


class Query(graphene.ObjectType):
    all_categories = graphene.List(CategoryType)
    all_ingredients = graphene.List(IngredientType)
    ingredient_by_name = graphene.Field(IngredientType, name=graphene.String(required=True))

    def resolve_all_ingredients(root, info):
        return Ingredient.objects.all()

    def resolve_all_categories(root, info):
        return Category.objects.all()

    def resolve_ingredient_by_name(root, info, name):
        try:
            return Ingredient.objects.get(name=name)
        except Ingredient.DoesNotExist:
            return None

schema = graphene.Schema(query=Query)