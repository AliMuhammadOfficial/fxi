from django.db import models
from django.conf import settings
import uuid
from django.core.validators import MinValueValidator

class AccountUser(models.Model):


	uid = models.UUIDField(
		unique=True,
		default=uuid.uuid4,
		verbose_name='Unique Identifier',
	)
	user = models.OneToOneField(
		settings.AUTH_USER_MODEL,
  	    on_delete=models.PROTECT,
  	)
	mobile = models.CharField(max_length=30)
	two_factor_auth = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_verified = models.BooleanField(default=False)
	is_deleted = models.BooleanField(default=False)
	activation_url = models.URLField()
	ref_by = models.UUIDField(
  	  	null=True,
  	  	verbose_name='Unique Identifier',
  	)
	created = models.DateTimeField(
		blank=True,
		auto_now_add=True
  	)
	modified = models.DateTimeField(
		blank=True,
		auto_now=True
	)
	def __str__(self):
  		return f"{self.user}"

class Account(models.Model):
    
	class Meta:
		verbose_name = 'Account'
		verbose_name_plural = 'Accounts'

	id = models.AutoField(
		primary_key=True,
	)
	uid = models.UUIDField(
		unique=True,
		editable=False,
		default=uuid.uuid4,
		verbose_name='Public identifier',
	)
	user = models.OneToOneField(
		settings.AUTH_USER_MODEL,
		on_delete=models.PROTECT,
	)
	balance = models.FloatField()
	created = models.DateTimeField(
		blank=True,
		auto_now_add=True
	)
	modified = models.DateTimeField(
		blank=True,
		auto_now=True
	)
	def __str__(self):
		return f"{self.user}"

class Action(models.Model):
	class Meta:
		verbose_name = 'Account Action'
		verbose_name_plural = 'Account Actions'

	ACTION_TYPE_DEPOSITED = 'DEPOSITED'
	ACTION_TYPE_WITHDRAWN = 'WITHDRAWN'
	ACTION_TYPE_CHOICES = (
		(ACTION_TYPE_DEPOSITED, 'Deposited'),
		(ACTION_TYPE_WITHDRAWN, 'Withdrawn'),
	)

	id = models.AutoField(
		primary_key=True,
	)
	user_friendly_id = models.CharField(
		unique=True,
		editable=False,
		max_length=30,
	)
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.PROTECT,
		help_text='User who performed the action.',
	)
	created = models.DateTimeField(
		blank=True,
		auto_now_add=True
	)
	account = models.ForeignKey(
		Account,
		on_delete=models.PROTECT
	)
	action_type = models.CharField(
		max_length=30,
		choices=ACTION_TYPE_CHOICES,
	)

	comment = models.TextField(
		blank=True,
	)

	debug_balance = models.FloatField()
	def __str__(self):
		return self.action_type
