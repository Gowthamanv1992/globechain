import graphene
from graphene_django import DjangoObjectType
import graphql_jwt
from django.contrib.gis.geos import Point
import json
from users.models import User, Profile

from django.contrib.gis.db import models
from graphene_django.converter import convert_django_field
from graphene import relay
from globechain import constants

class GeoJSON(graphene.Scalar):

    @classmethod
    def serialize(cls, value):
        location = "{{lat: {lat}, lng: {long}}}".format(lat=value[0],long=value[1])
        return str(location)


@convert_django_field.register(models.PointField)
def convert_field_to_geojson(field, registry=None):
    return graphene.Field(
        GeoJSON,
        description=field.help_text,
        required=not field.null)


class AccountTypesEnum(graphene.Enum):
    CP = 'Company'
    CH = 'Charity'
    IV = 'Individual'
    PB = 'public'


class UserType(DjangoObjectType):
    class Meta:
        model = User


class ProfileType(DjangoObjectType):
    account_type = graphene.String()

    class Meta:
        model = Profile

    def resolve_account_type(self, info, **kwargs):
        return AccountTypesEnum[self.account_type]._value_


class UserMutation(graphene.Mutation):

    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        full_address = graphene.String(required=True)
        account_type = graphene.String(required=True)
        location = graphene.String(required=False)

    @classmethod
    def mutate(cls, root, info, username, password, first_name, last_name, full_address, account_type, location):
        user = User(username=username)
        user.set_password(password)
        user.save()

        latitude = int(location[location.find(':') + 1 : location.find(',')])
        longitude = int(location[location.rfind(':') + 1 : location.find('}')])
        profile = Profile(user=user, location=Point(latitude, longitude), first_name=first_name, last_name=last_name,account_type=AccountTypesEnum.get(account_type)._name_, full_address=full_address)
        profile.save()

        return ''


class Mutation(graphene.ObjectType):
    login = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    create_user = UserMutation.Field()


class Query(graphene.ObjectType):
    me = graphene.Field(ProfileType)

    def resolve_me(self, info):
        user = info.context.user

        if user.is_anonymous:
            raise Exception('Not logged in!')
        
        return Profile.objects.get(user_id=user.id)


schema = graphene.Schema(mutation=Mutation,query=Query)

