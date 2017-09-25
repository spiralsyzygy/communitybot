from django.conf import settings
from django.db import models
from utils.mixins import TimeStampsMixin


class Membership(TimeStampsMixin, models.Model):
    member = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='group_memberships')
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    roles = models.ManyToManyField('Role', related_name='memberships')

    def __unicode__(self):
        return u"{0}, {1}, {2}".format(self.member.username, self.group.name, self.active)

INVITE_PENDING  = 0 # Default. Does nothing.
INVITE_ACCEPTED = 1 # Invited accepted. Creates membership
INVITE_DECLINED = 2 # Invited declined. Does nothing.
INVITE_EXPIRED  = 3 # Expired. Set by external timer.
INVITE_REVOKED  = 4 # Revoked. Sorry, you're uninvited.
INVITE_STATUSES = (
    (INVITE_PENDING, 'Invite Pending'),
    (INVITE_ACCEPTED, 'Invite Accepted'),
    (INVITE_DECLINED, 'Invite Declined'),
    (INVITE_EXPIRED, 'Invite Expired'),
    (INVITE_REVOKED, 'Invite Revoked')
)

class Invite(TimeStampsMixin, models.Model):
    group = models.ForeignKey('Group', related_name='invites')
    inviter = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name="membership_invites")
    invited = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='group_invitations')
    reason = models.CharField(max_length=64, null=True, blank=True)
    status = models.IntegerField(choices=INVITE_STATUSES, default=INVITE_PENDING)

    def accept(self):
        try:
            # Try creating the group Membership before saving.
            self.status = INVITE_ACCEPTED
            Membership.objects.create(group=self.group, member=self.invited)
            self.save()
        except:
            # TODO: Handle this better
            raise

    def decline(self):
        self.status = INVITE_DECLINED
        return self.save()

    def revoke(self):
        self.status = INVITE_REVOKED
        return self.save()

    def expire(self):
        self.status = INVITE_EXPIRED
        return self.save()


class Group(TimeStampsMixin, models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="created_groups")
    name = models.CharField(max_length=255, unique=True)
    about = models.TextField()
    is_active = models.BooleanField(default=True)
    private = models.BooleanField(default=False)
    memberships = models.ManyToManyField(
                                settings.AUTH_USER_MODEL,
                                through='Membership',
                                through_fields=('group', 'member'),
                                related_name='my_groups')


    def __unicode__(self):
        return "{0}: creator:{1}, private:{2}, members:{3}".format(
                        self.name, self.creator.username, self.private, self.member_count)

    @property
    def member_count(self):
        return Membership.objects.filter(group=self).count()

    def add_member(self, person):
        membership, created = Membership.objects.get_or_create(
                group=self,
                member=person)
        return membership

    def remove_member(self, person):
        membership = Membership.objects.filter(
                group=self,
                member=person).delete()

    def get_members(self, active=True):
        return self.members.filter(group=self, active=active)


# TODO: Integrate Django Guardian object permissions
# TODO: Define Django auth model groups for default role permission sets
# TODO: Try to keep all of this as extensible as humanly possible.

class Role(TimeStampsMixin, models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    group = models.ForeignKey('Group', related_name='roles')
    policies = models.ManyToManyField('Policy', related_name='roles')


class Policy(TimeStampsMixin, models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    group = models.ForeignKey('Group', related_name='policies')
