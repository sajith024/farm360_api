from django.contrib.auth import get_user_model

from django.db.models import Model
from django.db.models import CharField, TextField, ImageField, DateTimeField
from django.db.models import ForeignKey, CASCADE


# Create your models here.
class CommunityQuery(Model):
    QUERY_TYPE = (
        ("query", "Query"),
        ("suggestion", "Suggestion"),
    )
    title = CharField(max_length=200)
    description = TextField(max_length=1000)
    query_type = CharField(choices=QUERY_TYPE, default="query")
    created_by = ForeignKey(get_user_model(), on_delete=CASCADE, related_name="queries")

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class CommunityQueryImage(Model):
    query = ForeignKey(CommunityQuery, on_delete=CASCADE, related_name="images")
    image = ImageField(upload_to="community/query/images")

    def __str__(self) -> str:
        return self.query.title


class CommunityComment(Model):
    description = TextField(max_length=1000)
    created_by = ForeignKey(get_user_model(), on_delete=CASCADE)
    query = ForeignKey(CommunityQuery, on_delete=CASCADE, related_name="comments")
    main = ForeignKey(
        "self", related_name="threads", null=True, blank=True, on_delete=CASCADE
    )
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self) -> str:
        pre = "Thread" if self.main else "Main"
        return f"{pre} Reply {self.created_by.get_short_name()}"


class CommunityCommentImage(Model):
    comment = ForeignKey(CommunityComment, on_delete=CASCADE, related_name="images")
    image = ImageField(upload_to="community/comment/images")

    def __str__(self) -> str:
        return f"Image {self.comment}"
