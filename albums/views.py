from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Albums
from .serializers import AlbumSerializer,AlbumDetailSerializer
from rest_framework import status, permissions
from account.permissions import IsAuthor
from rest_framework.views import APIView
from django.http import Http404

class AlbumListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        albums = Albums.objects.all()
        serializer = AlbumDetailSerializer(albums, many=True)
        return Response(serializer.data)
    
class AlbumCreateView(generics.CreateAPIView):
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_author:
            return self.create(request, *args, **kwargs)
        else:
            return Response({"detail": "You do not have permission to create albums."},
                            status=status.HTTP_403_FORBIDDEN)
        
class AlbumDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get_object(self, pk):
        try:
            return Albums.objects.get(pk=pk)
        except Albums.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        album = self.get_object(pk)
        serializer = AlbumDetailSerializer(album)
        return Response(serializer.data)

    def delete(self, request, pk):
        album = self.get_object(pk)
        if request.user.is_authenticated and IsAuthor().has_object_permission(request, self, album):
            album.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "You do not have permission to delete this album."},
                            status=status.HTTP_403_FORBIDDEN)