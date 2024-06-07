from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models

class studentInfo(models.Model):
    studID = models.IntegerField(primary_key=True)
    lrn = models.CharField(max_length=12)
    lastname = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    middlename = models.CharField(max_length=50)
    degree = models.CharField(max_length=150)
    yearlvl = models.CharField(max_length=10)
    sex = models.CharField(max_length=10)
    emailadd = models.EmailField()
    contact = models.CharField(max_length=11)
    extension = models.CharField(max_length=10, default='N/A')
    birthday = models.DateField(blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
        
    def __str__(self):
        return f"{self.studID}"

class applicants(models.Model):
    studID = models.ForeignKey(studentInfo, on_delete=models.CASCADE)
    cor_file = models.FileField(upload_to='applicants/cor_pic/', blank=True, null=True)
    grade_file = models.FileField(upload_to='applicants/grade_pic/', blank=True, null=True)
    schoolid_file = models.FileField(upload_to='applicants/schoolid_pic/', blank=True, null=True)
    scholar_type = models.CharField(max_length=50)
    gpa = models.FloatField()
    note = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=10, default="PENDING")

class Requirement(models.Model):
    studID = models.ForeignKey(studentInfo, on_delete=models.CASCADE)
    semester = models.CharField(max_length=50)
    gpa = models.FloatField()
    cor_file = models.FileField(upload_to='cor_files/', blank=True, null=True)
    grade_file = models.FileField(upload_to='grade_files/', blank=True, null=True)
    schoolid_file = models.FileField(upload_to='schoolid_files/', blank=True, null=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    units = models.IntegerField(default=0)
    note = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=10, default="SCHOLAR")

class scholars(models.Model):
    SCHOLARSHIP_CHOICES = (
        ('CHED', (
            ('Full Merit', 'CHED - Full Merit'),
            ('Half Merit', 'CHED - Half Merit'),
            ('Tulong Dunong Program', 'CHED - Tulong Dunong Program'),
            ('Tertiary Education Subsidy', 'CHED - Tertiary Education Subsidy'),
            ('Coscho', 'CHED - Coscho'),
        )),
        ('LGU', (
            ('ATESAP', 'LGU - ATESAP'),
            ('DOST Undergrad', 'LGU - DOST Undergrad'),
            ('With High Honor', 'LGU - With High Honor'),
        )),
        ('NGU', (
            ("Nature's Spring Foundation Inc", 'NGU - Nature\'s Spring Foundation Inc'),
            ('Lifebank Foundation', 'NGU - Lifebank Foundation'),
        )),
    )

    scholar_ID = models.IntegerField(primary_key=True)
    studID = models.ForeignKey(studentInfo, on_delete=models.CASCADE)
    scholar_type = models.CharField(max_length=100, choices=SCHOLARSHIP_CHOICES)

    def __str__(self):
        return f"{self.scholar_ID}: {self.get_scholar_type_display()} - {self.studID.lastname}, {self.studID.firstname}"

    def clean(self):
        if scholars.objects.filter(scholar_ID=self.scholar_ID).exclude(studID=self.studID).exists():
            raise ValidationError('Scholar ID already exists and is assigned to another student.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class SemesterDetails(models.Model):
    SEMESTER_CHOICES = (
        ('1', '1st Semester'),
        ('2', '2nd Semester'),
    )

    scholar = models.ForeignKey(scholars, related_name='semester_details', on_delete=models.CASCADE)
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES, default='1')
    amount = models.IntegerField(default=0)
    gpa = models.FloatField()
    year = models.CharField(max_length=10, null=True)
    scholar_status = models.CharField(max_length=10, default="ACTIVE")
    remarks = models.TextField(null=True, blank=True)
    date_added = models.DateField(default=timezone.now)
    total_units_enrolled = models.IntegerField(null=True)

    class Meta:
        unique_together = ('scholar', 'semester')

    def __str__(self):
        return f"{self.scholar.scholar_ID} - {self.get_semester_display()}"

    def clean(self):
        if SemesterDetails.objects.filter(scholar=self.scholar, semester=self.semester).exclude(id=self.id).exists():
            raise ValidationError(f'{self.get_semester_display()} details already exist for this scholar.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
