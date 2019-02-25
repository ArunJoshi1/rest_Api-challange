from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import viewsets
from myapp.api.serializers import (UserSerializer,
                                   CreateSerializer,SignInSerializer,
                                   PostSerializer
                                   )
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from ..models import Post
from rest_framework.authentication import TokenAuthentication
# Create your views here.
class GetUserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateUserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            username = data['username']
            password = data['password']
            first_name = data['first_name']
            last_name = data['last_name']
            email = data['email']

            user = User.objects.create_user(username=username,
                                            password=password,
                                            first_name=first_name,
                                            last_name=last_name,
                                            email=email,
                                            )
            user.save()
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except Exception:
            return Response("user already exist ")
    def list(self, request, *args, **kwargs):
        return Response()



class SignIn(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignInSerializer
    def create(self, request, *args, **kwargs):
        data = request.data
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user:
            info = {
                "id": user.id,
                "first_name":user.first_name,
                "email":user.email
            }
            return Response(info)
        return Response("Incorrect User name or password")




    def list(self, request, *args, **kwargs):
        return Response('Enter User name and password')


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    def create(self, request, *args, **kwargs):
        data = request.data
        user = User.objects.get(username=data['user'])
        title = data['title']
        body  = data['body']
        image = data['image']
        token=Token.objects.get(user=user)
        print(token)
        post = Post.objects.create(user=user,title=title,body=body,image=image)
        post.save()
        serializer = PostSerializer(post)
        return Response(serializer.data)
