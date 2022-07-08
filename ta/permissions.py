from rest_framework.permissions import BasePermission

class IsCandidateUser(BasePermission):
    """
    UserType이 candidate인 유저만 가능
    """
    message = '지원자만 사용하실 수 있습니다.'
    
    def has_permission(self, request, view):
        print(request.user)

        try :
            user_type = request.user.user_type.user_type
        except:
            user_type = None
        
        return bool(request.user and user_type == "candidate" )