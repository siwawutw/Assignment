from django.db import models

# Create your models here.
#สร้าง TABLE Category มีฟิลด์ 2 ฟิลด์ 1. ID (auto) 2.name (ชื่อประเภทบทความ)
class Category (models.Model):
    name = models.CharField(max_length=255,unique=True)

    def __str__(self):
        return self.name