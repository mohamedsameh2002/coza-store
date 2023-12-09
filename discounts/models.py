import random
import string
from django.db import models

# Create your models here.
def random_code ():
    all_chars = string.ascii_letters + string.digits 
    serial_list = [random.choice(all_chars) for _ in range(8)]
    serial_string = ''.join(serial_list)
    return serial_string

class Discount_codes (models.Model):
    code=models.CharField(max_length=10,default=random_code)
    discount=models.IntegerField(max_length=100)
    validate_from=models.DateTimeField(null=True,blank=True)
    validate_to=models.DateTimeField(null=True,blank=True)
    active=models.BooleanField(default=True)
    def __str__(self) -> str:
        return self.code