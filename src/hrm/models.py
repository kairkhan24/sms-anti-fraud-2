from django.db import models
from django.db.models import QuerySet


class AdminSettingsManager(models.Manager):
    def get_not_send_sms_phone_numbers(self) -> QuerySet:
        phone_numbers = PhoneNumber.objects.filter(is_enable=False)
        return phone_numbers
    
    def get_sms_limit_enable(self) -> QuerySet:
        phone_numbers = PhoneNumber.objects.filter(is_enable=True)
        return phone_numbers

    def get_sms_limit_period_in_seconds(self, period_in_seconds: int = 240) -> QuerySet:
        qs = PhoneNumber.objects.filter(setting__period_in_seconds=period_in_seconds)
        return qs

    def get_sms_limit_count_per_user(self, count_per_user: int = 10) -> QuerySet:
        qs = PhoneNumber.objects.filter(setting_count_per_user=count_per_user)
        return qs


class AdminSettings(models.Model):
    name = models.CharField(
        max_length=64,
        unique=True,
        verbose_name='Название конфигурации'
    )
    period_in_seconds = models.PositiveBigIntegerField()
    count_per_user = models.PositiveIntegerField()

    objects = AdminSettingsManager()

    def __str__(self):
        return self.name


class PhoneNumber(models.Model):
    phone_number = models.CharField(max_length=32, unique=True) # temp
    setting = models.ForeignKey(
        AdminSettings,
        on_delete=models.CASCADE,
        related_name='phone_numbers',
        verbose_name='Конфигурация'
    )
    is_enable = models.BooleanField(
        default=True,
        verbose_name='Может ли принимать смски?'
    )

    def __str__(self):
        return self.phone_number
