from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from university.services import WorkloadService

User = get_user_model()

@login_required
def staff_list_api(request):
    """
    API to get list of staff for a specific department (or all) with workload status.
    Query Params:
    - department_id: Filter by department
    - role: Filter by role (e.g. LECTURER)
    """
    department_id = request.GET.get('department_id')
    department_ids = request.GET.get('department_ids')
    role = request.GET.get('role')
    
    users = User.objects.filter(is_active=True)
    
    if department_ids:
        ids = []
        for raw_id in department_ids.split(','):
            raw_id = raw_id.strip()
            if raw_id.isdigit():
                ids.append(int(raw_id))
        if ids:
            users = users.filter(department_id__in=ids)
    elif department_id:
        users = users.filter(department_id=department_id)
        
    if role:
        # Map simple role name to DB constant if needed, or assume direct match
        # For safety, let's look up choices
        if role == 'LECTURER':
            users = users.filter(role=User.Role.LECTURER)
        elif role == 'HOD':
            users = users.filter(role=User.Role.HOD)
            
    data = []
    for user in users:
        status_data = WorkloadService.get_workload_status(user)
        data.append({
            'id': user.id,
            'name': user.get_full_name() or user.username,
            'email': user.email,
            'role': user.get_role_display(),
            'workload': status_data
        })
        
    return JsonResponse({'staff': data})
