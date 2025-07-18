from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from datetime import date
from collections import Counter
from django.db.models import Avg
from ..utils.pagination import CustomPageNumberPagination

from ..models import Application
from ..serializers import ApplicationSerializer, ApplicationCreateUpdateSerializer, ApplicationStatsSerializer, ApplicationAnalyticsSerializer
from ..mixins import ObjectManager, APIResponse
from ..mixins.audit import AuditMixin


class ApplicationAPIView(ObjectManager, AuditMixin):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, application_id=None):
        """GET /applications/ - List all applications with pagination and search
           GET /applications/{id}/ - Get specific application"""
        try:
            if application_id:
                # Get specific application
                application = get_object_or_404(Application, id=application_id, user=request.user)
                serializer = ApplicationSerializer(application)
                return APIResponse.success(data=serializer.data)
            else:
                # Get all applications for user, with search and pagination
                applications = Application.objects.filter(user=request.user)
                search_query = request.GET.get('search')
                if search_query:
                    from django.db.models import Q
                    applications = applications.filter(
                        Q(company__icontains=search_query) | Q(position__icontains=search_query)
                    )
                    
                # Pagination
                paginator = CustomPageNumberPagination()
                page = paginator.paginate_queryset(applications, request)
                serializer = ApplicationSerializer(page, many=True)
                return APIResponse.success(data={
                    'results': serializer.data,
                    'pagination': {
                        'page': paginator.page.number,
                        'page_size': paginator.page.paginator.per_page,
                        'total': paginator.page.paginator.count,
                        'total_pages': paginator.page.paginator.num_pages,
                    }
                })
        except Exception as e:
            return APIResponse.error(message="Failed to fetch applications")
    
    def post(self, request):
        """POST /applications/ - Create new application"""
        try:
            serializer_result = self.validate_serializer(
                ApplicationCreateUpdateSerializer, 
                request.data,
                context={'request': request}
            )
            
            if isinstance(serializer_result, ApplicationCreateUpdateSerializer):
                application = serializer_result.save()
                response_serializer = ApplicationSerializer(application)
                return APIResponse.success(data=response_serializer.data, status_code=status.HTTP_201_CREATED)
            else:
                return serializer_result
        except Exception as e:
            # Print the real error to the console for debugging
            print("Create application error:", e)
            return APIResponse.error(message=f"Failed to create application: {e}")
    
    def put(self, request, application_id):
        """PUT /applications/{id}/ - Update specific application"""
        try:
            application = get_object_or_404(Application, id=application_id, user=request.user)
            serializer_result = self.validate_serializer(
                ApplicationCreateUpdateSerializer,
                request.data,
                instance=application
            )
            
            if isinstance(serializer_result, ApplicationCreateUpdateSerializer):
                updated_application = serializer_result.save()
                response_serializer = ApplicationSerializer(updated_application)
                return APIResponse.success(data=response_serializer.data)
            else:
                return serializer_result
        except Exception as e:
            return APIResponse.error(message="Failed to update application")
    
    def delete(self, request, application_id):
        """DELETE /applications/{id}/ - Delete specific application"""
        try:
            application = get_object_or_404(Application, id=application_id, user=request.user)
            application.delete()
            return APIResponse.success(message="Application deleted successfully")
        except Exception as e:
            return APIResponse.error(message="Failed to delete application")
        

class ApplicationStatsAPIView(ObjectManager, AuditMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        applications = Application.objects.filter(user=user)
        total = applications.count()
        interviews = applications.filter(status=Application.Status.INTERVIEW).count()
        accepted = applications.filter(status=Application.Status.ACCEPTED).count()
        rejected = applications.filter(status=Application.Status.REJECTED).count()
        # Upcoming interviews: status=INTERVIEW and interview_date >= today
        today = date.today()
        upcoming_qs = applications.filter(status=Application.Status.INTERVIEW, interview_date__gte=today).order_by('interview_date')
        upcoming = [
            {
                'company': app.company,
                'position': app.position,
                'interview_date': app.interview_date.strftime('%Y-%m-%d') if app.interview_date else None
            }
            for app in upcoming_qs
        ]
        data = {
            'total_applications': total,
            'interviews_scheduled': interviews,
            'accepted_applications': accepted,
            'rejected_applications': rejected,
            'upcoming_interviews': upcoming,
        }
        serializer = ApplicationStatsSerializer(data)
        return APIResponse.success(data=serializer.data)     


class ApplicationAnalyticsAPIView(ObjectManager, AuditMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """GET /applications/analytics/ - Analytics for applications"""
        user = request.user
        applications = Application.objects.filter(user=user)
        total = applications.count() or 1  # avoid division by zero

        # Get all possible choices from the model
        status_choices = [choice[0] for choice in Application.Status.choices]
        job_type_choices = [choice[0] for choice in Application.JobType.choices]

        # Status counts and percentages
        status_counter = Counter(applications.values_list('status', flat=True))
        status_counts = {
            status: {
                "count": status_counter.get(status, 0),
                "percent": round(100 * status_counter.get(status, 0) / total, 2)
            }
            for status in status_choices
        }

        # Job type counts and percentages
        job_type_counter = Counter(applications.values_list('job_type', flat=True))
        job_type_counts = {
            job_type: {
                "count": job_type_counter.get(job_type, 0),
                "percent": round(100 * job_type_counter.get(job_type, 0) / total, 2)
            }
            for job_type in job_type_choices
        }

        # Average salary by job type
        avg_salary_by_job_type = {}
        for job_type in job_type_choices:
            avg_salary = applications.filter(job_type=job_type, salary__isnull=False).aggregate(avg=Avg('salary'))['avg']
            avg_salary_by_job_type[job_type] = round(avg_salary or 0, 2)

        data = {
            "status_counts": status_counts,
            "job_type_counts": job_type_counts,
            "avg_salary_by_job_type": avg_salary_by_job_type,
        }
        serializer = ApplicationAnalyticsSerializer(data)
        return APIResponse.success(data=serializer.data)