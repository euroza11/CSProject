from django.db import models

class Card(models.Model):
    TYPE = [
        ('Normal-Unit', 'Normal-Unit'),
        ('Trigger-Unit', 'Trigger-Unit'),
        ('G-Guardian', 'G-Guardian'),
        ('G-Unit', 'G-Unit'),
        ('Normal-Order', 'Normal-Order'),
        ('Set-Order', 'Set-Order'),
        ('Blitz-Order', 'Blitz-Order'),
        ('Trigger-Order', 'Trigger-Order'),
        # add more types if needed
    ]
    NATION = [
        ('Keter Sanctuary', 'Keter Sanctuary'),
        ('Dragon Empire', 'Dragon Empire'),
        ('Stoicheia', 'Stoicheia'),
        ('Dark State', 'Dark State'),
        ('Brandt Gate', 'Brandt Gate'),
        ('Lyrical Monasterio', 'Lyrical Monasterio'),
        ('No Nation', 'No Nation'),
        # add more as needed
    ]
    GRADE = [
        (0, 'Grade 0'),
        (1, 'Grade 1'),
        (2, 'Grade 2'),
        (3, 'Grade 3'),
        (4, 'Grade 4'),
        (5, 'Grade 5'),
        (10, 'Grade 10'),
        (11, 'Grade 11'),
        # add more as needed
    ]
    
    name = models.CharField(max_length=100)
    card_type = models.CharField(max_length=50, choices=TYPE, null=True)
    nation = models.CharField(max_length=50, choices=NATION, null=True)
    grade = models.IntegerField(choices=GRADE, null=True)  # 0 to 4
    power = models.IntegerField(blank=True, null=True)
    shield = models.IntegerField(blank=True, null=True)
    skill = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='cards/', blank=True, null=True)

    def __str__(self):
        return self.name
