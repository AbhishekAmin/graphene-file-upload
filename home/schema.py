import graphene
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload

from home.models import Files


class FilesType(DjangoObjectType):
    class Meta:
        model = Files


class Query(graphene.ObjectType):
    all_files = graphene.List(FilesType)

    def resolve_all_files(self, info):
        return Files.objects.all()


class UploadFileMutation(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    success = graphene.Boolean()

    def mutate(self, info, **kwargs):
        success = False
        file = kwargs.get("file")
        print("****** FILE *******")
        print("Filename:", file.name)
        print("Size:", file.size)

        created_file = Files.objects.create(file=file)
        if created_file:
            success = True

        return UploadFileMutation(success=success)


class Mutation(graphene.ObjectType):
    upload_file = UploadFileMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
