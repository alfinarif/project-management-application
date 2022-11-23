from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_quill.fields import QuillField


# created user Custom Manager
class UserManager(BaseUserManager):
    # this function will create users objects
    def create_user(self, email, password, **extra_fields):
        if not email:
            # raise value error if email address is empty
            raise ValueError("A valid email address is required")

        user = self.model(
            email=self.normalize_email(email),  # normalize submited email address
            **extra_fields
        )
        user.set_password(password)  # set_password will converting char-password to hash
        user.save(using=self._db)  # save user info to current database
        return user  # finally return the user object

        # this function will create super user for admin

    def create_superuser(self, email, password, **extra_fields):
        # set all access to admin users
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('superuser must be is_staff=True')
        if extra_fields.get('is_active') is not True:
            raise ValueError('superuser must be is_active=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('superuser must be is_superuser=True')

        return self.create_user(email, password, **extra_fields)  # create super user object using create_user function


# created custom user models
class User(AbstractBaseUser, PermissionsMixin):
    # users type tuples
    USER_TYPE = (
        ('admin', 'admin'),
        ('leader', 'leader'),
        ('worker', 'worker')
    )
    email = models.EmailField(unique=True, blank=False, null=False)
    user_type = models.CharField(max_length=100, choices=USER_TYPE, default='worker')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # we can pass extra fields on this list
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()  # called our custom manager here

    def __str__(self):
        return f"{self.email}"  # return a string that we can see on dashboard

    class Meta:
        verbose_name_plural = "Users List"  # verbose_name_plural will replace your models name


# created user profile models
class Profile(models.Model):
    SEX_TYPE = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Others')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='profile')  # relation between user and profile models
    full_name = models.CharField(max_length=255, blank=False, null=False)
    surname = models.CharField(max_length=255, blank=False, null=False)
    fathers_name = models.CharField(max_length=255, blank=False, null=False)
    mothers_name = models.CharField(max_length=255, blank=False, null=False)
    date_of_birth = models.DateField(null=True, blank=True)
    sex_name = models.CharField(max_length=55,choices=SEX_TYPE, blank=False, null=False)
    phone = models.CharField(max_length=14, blank=False, null=False)
    postel_code= models.CharField(max_length=14, blank=False, null=False)
    nid_card_no = models.CharField(max_length=14, blank=False, null=False)
    city = models.CharField(max_length=255, blank=False, null=False)
    address = models.CharField(max_length=300, blank=False, null=False)
    nationality = models.CharField(max_length=55, blank=False, null=False)
    marital_Status = models.BooleanField(default=False)
    employe_image = models.ImageField()

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email  # return a string that we can see on dashboard

    def is_fully_filled(self):
        field_names = [f.name for f in self._meta.get_fields()]
        for field_name in field_names:
            value = getattr(self, field_name)
            if value is None or value == '':
                return False
        return True

        
    class Meta:
        verbose_name_plural = 'Users Profiles'  # verbose_name_plural will replace your models name
    

    # signals functions
    """
    once a user object create,
    profile object will create for each user object
    """

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)  # creating profile object

    @receiver(post_save, sender=User)
    def save_profile(sender, instance, **kwargs):
        instance.profile.save()  # save profile object

# bank info model
class Bank(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE,
                                related_name='bank')  # relation between user and profile models
    bank_name = models.CharField(max_length=255, blank=False, null=False)
    bank_acc_num = models.CharField(max_length=255, blank=False, null=False)
    acc_holder_name = models.CharField(max_length=255, blank=False, null=False)
    acc_branch_name = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return self.profile.user.email  # return a string that we can see on dashboard
    
    class Meta:
        verbose_name_plural = 'Users Bank Info'  # verbose_name_plural will replace your models name

    @receiver(post_save, sender=Profile)
    def create_bank(sender, instance, created, **kwargs):
        if created:
            Bank.objects.create(profile=instance)  # creating profile object

    @receiver(post_save, sender=Profile)
    def save_bank(sender, instance, **kwargs):
        instance.bank.save()  # save profile object


#notification model
class Notification(models.Model):
    subject = models.CharField(max_length=255, blank=False, null=False)
    from_admin = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='from_admin')
    from_leader = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='from_leader')
    to_leader = models.ManyToManyField(User, blank=True, related_name='to_leader')
    to_worker = models.ManyToManyField(User, blank=True, related_name='to_worker')
    is_active = models.BooleanField(default=False)
    is_seen = models.BooleanField(default=False)
    message = models.TextField(max_length=500, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.subject

