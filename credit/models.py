from django.db import models
from django.db.models import TextChoices
# Create your models here.


class Program(models.Model):
    min_sum = models.PositiveIntegerField()
    max_sum = models.PositiveIntegerField()
    min_year = models.PositiveSmallIntegerField()
    max_year = models.PositiveSmallIntegerField()

    def __str__(self):
        return 'Минимальная и максимальная суммы: {0}/{1}. Минимальный и максимальный возраст: {2}/{3}'\
            .format(self.min_sum, self.max_sum, self.min_year, self.max_year)


class Borrower(models.Model):
    iin = models.CharField(max_length=12)
    date_birth = models.DateField()

    def __str__(self):
        return 'ИИН {0}'.format(self.iin)


class StatusTypes(TextChoices):
    approved = 'approved', 'Одобрено'
    denied = 'denied', 'Отказано'


class Application(models.Model):
    summa = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=StatusTypes.choices)
    program = models.ForeignKey(Program, blank=True, null=True, on_delete=models.CASCADE, related_name='program')
    borrower = models.ForeignKey(Borrower, on_delete=models.DO_NOTHING, null=True, blank=True)
    rejection_reason = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return 'Сумма: {0}, Статус: {1}, Программа: {2}, Заемщик: {3}, Причина: {4}'\
            .format(self.summa, self.status, self.program, self.borrower, self.rejection_reason)


class Blacklist(models.Model):
    iin = models.CharField(max_length=12)

    def __str__(self):
        return 'ИИН черного списка: {0}'.format(self.iin)
