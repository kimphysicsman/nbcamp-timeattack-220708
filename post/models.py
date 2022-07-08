from venv import create
from django.db import models
from user.models import User


class SkillSet(models.Model):
    name = models.CharField(max_length=128)
    job_posts = models.ManyToManyField('JobPost', through='JobPostSkillSet')

    class Meta:
        db_table = 'skill_sets'

# "jobpostskillset_set"   JobPostSkillSet -> jobpostskillset_set
class JobPostSkillSet(models.Model):
    skill_set = models.ForeignKey('SkillSet', on_delete=models.SET_NULL, null=True)
    job_post = models.ForeignKey('JobPost', on_delete=models.SET_NULL, null=True)


class JobType(models.Model):
    job_type = models.CharField(max_length=128)  # permanent temporary

    class Meta:
        db_table = 'job_types'


class JobPost(models.Model):
    job_type = models.ForeignKey(JobType, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True)
    job_description = models.TextField()
    salary = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'job_posts'


class Company(models.Model):
    company_name = models.CharField(max_length=128)
    business_area = models.ManyToManyField('BusinessArea', through='CompanyBusinessArea')

    class Meta:
        db_table = 'companies'


class CompanyBusinessArea(models.Model):
    company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True)
    business_area = models.ForeignKey('BusinessArea', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'company_business_areas'


class BusinessArea(models.Model):
    area = models.CharField(max_length=128)

    class Meta:
        db_table = 'business_areas'


class JobApplication(models.Model):
    candidate = models.ForeignKey(User, verbose_name="지원자", on_delete=models.CASCADE)
    jobpost = models.ForeignKey(JobPost, verbose_name="채용 공고",on_delete=models.CASCADE)
    created_at = models.DateTimeField("지원일", auto_now_add=True)

    class Meta:
        db_table = 'job_applications'