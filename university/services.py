from .models import TaskForce, WorkloadSettings
from django.db.models import Sum
from django.db import models

class WorkloadService:
    @staticmethod
    def calculate_workload(user):
        """
        Calculates the total weightage of ACTIVE or DRAFT task forces directly assigned to the user.
        Excludes task forces in other states (e.g. inactive, completed concepts).
        """
        # We only count ACTIVE and DRAFT task forces for workload
        # (Assuming DRAFT also counts because HOD is planning with them)
        # OR: Should we only count ACTIVE? 
        # Requirement says "Active Task Forces". Let's stick to ACTIVE and SUBMITTED/APPROVED.
        # Drafts are tricky. Let's include everything that is NOT Inactive or Rejected.
        
        relevant_statuses = ['ACTIVE', 'SUBMITTED', 'APPROVED', 'DRAFT']
        
        # Calculate as Member
        member_weightage = TaskForce.objects.filter(
            members=user,
            status__in=relevant_statuses
        ).aggregate(total=Sum('weightage'))['total'] or 0
        
        # Calculate as Chairman (If chairman also gets workload points?)
        # Use Case doesn't explicitly say Chairman gets separate points, but typically they do.
        # But the TaskForce model links chairman separately. 
        # If chairman is also in members list, we might double count.
        # Let's assume Chairman is implicitly a member or explicitly added to members.
        # For safety, let's just sum up distinct task forces where user is EITHER chairman OR member.
        
        task_forces = TaskForce.objects.filter(
            status__in=relevant_statuses,
            members=user
        ).distinct()
        
        total_weightage = task_forces.aggregate(total=Sum('weightage'))['total'] or 0
        return total_weightage

    @staticmethod
    def get_workload_status(user, additional_weightage=0):
        """
        Returns a dictionary with status, color, and message.
        additional_weightage: Used to simulate "What if I add this task force?"
        """
        current_weightage = WorkloadService.calculate_workload(user)
        predicted_total = current_weightage + additional_weightage
        
        settings = WorkloadSettings.objects.first()
        if not settings:
            # Fallback if no settings exist
            return {
                'status': 'UNKNOWN',
                'color': 'secondary',
                'message': 'Workload settings not configured'
            }
            
        if predicted_total > settings.max_weightage:
            return {
                'status': 'OVERLOADED',
                'color': 'danger',
                'message': f'Overloaded ({predicted_total}/{settings.max_weightage})'
            }
        elif predicted_total < settings.min_weightage:
            return {
                'status': 'UNDERLOADED',
                'color': 'warning',
                'message': f'Underloaded ({predicted_total}/{settings.max_weightage})'
            }
        else:
            return {
                'status': 'BALANCED',
                'color': 'success',
                'message': f'Balanced ({predicted_total}/{settings.max_weightage})'
            }
