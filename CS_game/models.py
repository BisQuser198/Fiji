from django.db import models

# Create your models here.
# created CS_game/forms.py

class Employee(models.Model):
    # Mirror the columns in your firma.sql table
    name          = models.CharField(max_length=100)
    department_id = models.IntegerField()
    manager_id    = models.IntegerField()
    salary        = models.DecimalField(max_digits=10, decimal_places=2)
    promotable = models.BooleanField(default=False)

    class Meta:
        db_table = 'employee'   # matches the table name in firma.sql
#         managed  = False        # Django won’t try to create/drop this table
# •	managed = False tells Django not to run migrations on this table.
