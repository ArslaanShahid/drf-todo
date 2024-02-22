from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Todo
from .serializer import TodoSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class TodoView(APIView):
    authenticate_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        
        user = request.user
        todos = Todo.objects.filter(user = user)
        serializer = TodoSerializer(todos, many=True)
        return Response({
            'status': True,
            'data': serializer.data,
            'messsage': 'todo fetched successfully'
        })
    
    def post(self, request):
        try:
            user = request.user
            data = request.data
            data['user'] = user.id
            serializer = TodoSerializer(data = data)
            
            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'invalid fields',
                    'data': serializer.errors
                })
                
            serializer.save()
            return Response({
                'status':True,
                'message': 'Todo is Created',
                'data':serializer.data
            })
            
        except Exception as e:
            return Response({
                'status': False,
                'message': 'something went wrong',
                'data':{}
            })
    def patch(self, request):
        try:
            data = request.data
            if not data.get('uid'):
                return Response({
                    'status':False,
                    'message': 'something went wrong',
                    'data':{}

                })
            obj = Todo.objects.filter(uid = data.get('uid'))
            if not obj.exists():
                return Response({
                    'status':False,
                    'message': 'invalid uid',
                    'data':{}

                })
            serializer = TodoSerializer(obj[0], data=data, partial=True)
            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'invalid fields',
                    'data': serializer.errors
                })
                
            serializer.save()
            return Response({
                'status':True,
                'message': 'Todo is Updated',
                'data':serializer.data
            })
        except Exception as e:
            print(e)
            return Response({
                'status': False,
                'message': 'something went wrong',
                'data':{}
            })