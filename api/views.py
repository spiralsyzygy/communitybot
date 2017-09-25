from rest_framework import viewsets
from people.models import Person
from posts.models import Post, Comment
from groups.models import Group, Membership, Invite, Role
from .serializers import (
        NestedPersonSerializer,
        NestedCommentSerializer,
        CommentSerializer,
        PostSerializer,
        GroupSerializer,
)


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all().order_by('-date_joined')
    serializer_class = NestedPersonSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-date_created')
    serializer_class = PostSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('-date_created')
    serializer_class = GroupSerializer
