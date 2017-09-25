from posts.models import Post, Comment
from people.models import Person, Connection
from groups.models import Group, Membership, Invite, Role
from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

class PersonSerializer(serializers.ModelSerializer):
    post_count = serializers.IntegerField()
    class Meta:
        model = Person
        fields = ('url', 'username',
                  'first_name', 'last_name',
                  'email', 'screen_name', 'post_count')


class NestedPersonSerializer(serializers.ModelSerializer):
    followers = PersonSerializer(many=True, read_only=True)
    following = PersonSerializer(many=True, read_only=True)
    posts = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='post-detail')
    post_count = serializers.IntegerField()
    class Meta:
        model = Person
        fields = ('url', 'username',
                  'first_name', 'last_name',
                  'email', 'screen_name', 'post_count',
                  'followers', 'following',
                  'posts')


class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = ('from_person', 'to_person', 'status')


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ('parent_id', 'text', 'author', 'date_created', 'date_modified')
    author = serializers.HyperlinkedIdentityField(view_name='person-detail')


class NestedCommentSerializer(NestedHyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ('parent_id', 'text', 'author', 'date_created', 'date_modified', 'comments')
    comments = CommentSerializer(many=True, read_only=True)
    author = serializers.HyperlinkedIdentityField(view_name='person-detail')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('text', 'author', 'slug', 'approved', 'comments')
    comments = NestedCommentSerializer(many=True, read_only=True)
    author = serializers.HyperlinkedIdentityField(view_name='person-detail')

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('creator', 'name', 'about', 'is_active', 'private', 'memberships')
    creator = serializers.HyperlinkedIdentityField(view_name='person-detail')
    memberships = PersonSerializer(many=True, read_only=True)
