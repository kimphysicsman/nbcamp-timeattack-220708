from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status

from .models import (
    JobPostSkillSet,
    JobType,
    JobPost,
    Company,
    JobApplication,
)
from .serializers import JobPostSerializer, JobApplicationSerializer
from django.db.models.query_utils import Q

from ta.permissions import IsCandidateUser
from rest_framework_simplejwt.authentication import JWTAuthentication

class SkillView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        skills = request.query_params.getlist('skills', '')
        print("skills = ", end=""), print(skills) # ["mysql","python"]

        # job_skills = JobPostSkillSet.objects.filter(
        #     Q(skill_set__name='python') | Q(skill_set__name='mysql')
        # )

        query = Q()  # Q(skill_set__name='python') | Q(skill_set__name='mysql') | Q
        for skill in skills:
            query.add(Q(skill_set__name=skill), Q.OR)

        job_skills = JobPostSkillSet.objects.filter(query)

        job_posts = JobPost.objects.filter(
            id__in=[job_skill.job_post.id for job_skill in job_skills]
        )

        if job_posts.exists():
            serializer = JobPostSerializer(job_posts, many=True)
            return Response(serializer.data)

        return Response(status=status.HTTP_404_NOT_FOUND)


class JobView(APIView):

    def post(self, request):
        job_type = int(request.data.get("job_type", None))
        # job_type = request.data.get("job_type", None)
        company_name = request.data.get("company_name", None)

        # 직업 유형 처리
        job_type_qs = JobType.objects.filter(id=job_type)
        # job_type_qs = JobType.objects.filter(job_type=job_type)
        if not job_type_qs.exists():
            return Response({"message": "invalid job type"}, status=status.HTTP_400_BAD_REQUEST)

        # 회사 이름 처리
        company = Company.objects.filter(company_name=company_name)
        if not company.exists():
            company = Company(company_name=company_name).save()
        else:
            company = company.first()

        # request.data.pop('job_type', None)
        job_serializer = JobPostSerializer(data=request.data)
        if job_serializer.is_valid():
            job_serializer.save(company=company, job_type=job_type_qs.first())
            return Response(status=status.HTTP_200_OK)

        return Response(job_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 채용 지원 기능
class ApplicationView(APIView):
    permission_classes = [IsCandidateUser]
    
    authentication_classes = [JWTAuthentication]
    # 채원 지원
    def post(self, request):
        job_post_id = request.data.get('job_post', "")
        user = request.user
        
        job_post = JobPost.objects.filter(id=job_post_id)

        if 0 < len(job_post):
            job_post = job_post.first()
        else:
            return Response({"error": "job_post가 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            'candidate': user.id
        }

        job_application_serializer = JobApplicationSerializer(data=data)

        if job_application_serializer.is_valid():
            job_application_serializer.save(jobpost=job_post)

            return Response({'message': '저장 완료!'}, status=status.HTTP_200_OK)

        return Response(job_application_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # job_application = JobApplication.objects.create(candidate=user, jobpost=job_post)

        # return Response(JobApplicationSerializer(job_application).data, status=status.HTTP_200_OK)