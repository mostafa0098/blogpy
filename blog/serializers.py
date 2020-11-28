from rest_framework import serializers


class SingleArticleSerializer(serializers.Serializer):
    title = serializers.CharField(
        required=True, max_length=50, allow_null=False, allow_blank=False)
    cover = serializers.CharField(
        required=True, max_length=250, allow_null=False, allow_blank=False)
    content = serializers.CharField(
        required=True, max_length=2500, allow_null=False, allow_blank=False)
    created_at = serializers.DateTimeField(
        required=True, allow_null=False)


class SubmitArticleSerializer(serializers.Serializer):
    title = serializers.CharField(
        required=True, max_length=50, allow_null=False, allow_blank=False)
    cover = serializers.FileField(
        required=True, allow_empty_file=False)
    content = serializers.CharField(
        required=True, max_length=2500, allow_null=False, allow_blank=False)
    category_id = serializers.IntegerField(required=True, allow_null=False)
    author_id = serializers.IntegerField(required=True, allow_null=False)
    promote = serializers.BooleanField(required=True, allow_null=False)


class UpdateArticleCoverSerializer(serializers.Serializer):
    article_id = serializers.IntegerField(required=True, allow_null=False)
    cover = serializers.FileField(
        required=True,  allow_empty_file=False)


class DeleteArticleCoverSerializer(serializers.Serializer):
    article_id = serializers.IntegerField(required=True, allow_null=False)
