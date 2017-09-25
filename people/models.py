from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from utils.mixins import TimeStampsMixin

class Person(AbstractUser):
    screen_name = models.CharField(max_length=255)
    connections = models.ManyToManyField('self', through='Connection',
                                         symmetrical=False,
                                         related_name='connected_to')

    def __unicode__(self):
        return u"{0} {1} active: {2}".format(self.username, self.email, self.is_active)

    def add_connection(self, person, status):
        connection, created = Connection.objects.get_or_create(
            from_person=self,
            to_person=person,
            status=status)
        return connection

    def remove_connection(self, person, status):
        connection = Connection.objects.filter(
                from_person=self,
                to_person=person,
                status=status).delete()

    def get_connections(self, status):
        return self.connections.filter(
                to_people__status=status,
                to_people__from_person=self)

    def get_connected_to(self, status):
        return self.connected_to.filter(
                from_people__status=status,
                from_people__to_person=self)

    def follow(self, person):
        return self.add_connection(person, CONNECTION_FOLLOWING)

    def unfollow(self, person):
        return remove_connection(person, CONNECTION_FOLLOWING)

    def get_groups(self):
        return self.group_memberships.filter(
            member=self,
            active=True
            )

    def get_posts(self):
        return self.posts.all().order_by('date_created')

    @property
    def following(self):
        return self.get_connections(CONNECTION_FOLLOWING)

    @property
    def followers(self):
        return self.get_connected_to(CONNECTION_FOLLOWING)

    @property
    def blocked_followers(self):
        return self.get_connected_to(CONNECTION_BLOCKED)

    @property
    def posts(self):
        return self.get_posts()

    @property
    def post_count(self):
        return self.get_posts().count()

    @property
    def groups(self):
        return self.my_groups.all()


CONNECTION_FOLLOWING = 1
CONNECTION_BLOCKED = 2
CONNECTION_STATUSES = (
    (CONNECTION_FOLLOWING, 'Following'),
    (CONNECTION_BLOCKED, 'Blocked'),
)


class Connection(TimeStampsMixin, models.Model):
    from_person = models.ForeignKey(Person,
                    related_name='from_people', on_delete=models.CASCADE)
    to_person = models.ForeignKey(Person,
                    related_name='to_people', on_delete=models.CASCADE)
    status = models.IntegerField(choices=CONNECTION_STATUSES)

    class Meta:
        unique_together=('from_person', 'to_person', 'status')

    def save(self, *args, **kwargs):
        if self.from_person == self.to_person:
            raise ValidationError('You can\'t have yourself as a connection!')
        return super(Connection, self).save(*args, **kwargs)
