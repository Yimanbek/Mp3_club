from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.files.base import ContentFile
from pydub import AudioSegment
from .models import Music
from .serializers import MusicSerializer,MusicOutputSerializer1,MusicOutputSerializer
from .models import Albums  # Импорт из текущего приложения
from category.models import Category
import io
from account.permissions import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404
from rest_framework.generics import DestroyAPIView
from rest_framework import permissions
from django.shortcuts import render,redirect
from rest_framework.decorators import action
from like.models import Like
from like.serializers import LikeSerializer
from rest_framework import viewsets
from django.shortcuts import get_object_or_404


import logging
logger = logging.getLogger(__name__)






#For Post in PostMan
class MusicView(APIView):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            if not request.user.is_author:
                return Response({'error': 'You are not an author!'}, status=401)
            if request.data.get('in_album'):
                try:
                    album = Albums.objects.get(title=request.data['in_album'])
                except Albums.DoesNotExist:
                    return Response({'error': 'This album is not found.'}, status=404)
                
                if album.owner != request.user:
                    return Response({'error': 'You are not the author of this album'}, status=401)

                if 'audio_file' not in request.FILES:
                    return Response({'error': 'Audio file not found in the request.'}, status=400)

                audio_file = request.FILES['audio_file']

              
                audio = AudioSegment.from_mp3(io.BytesIO(audio_file.read()))
                compressed_audio = audio.export(format='mp3', bitrate='64k')

                category_name = request.data.get('category')
                category, created = Category.objects.get_or_create(name=category_name)

                music_instance = Music(
                    name_music = request.data.get('name_music'),
                    audio_file=ContentFile(compressed_audio.read(), name='audio.mp3'),  
                    image_music = request.data.get('image_music') if 'image_music' in request.data else '/music/defaul_image/sEZB30zciy5YEGCrSUPkhKNMjcXUm7YdvC0PwpwIYZ3CRmhrXUDBnGwbKnN-ya9Z4VSnrqwe.jpg',
                    author=request.user,  
                    category=category,  
                    in_albums=album
                )
                music_instance.save()

                return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
            else:
                if 'audio_file' not in request.FILES:
                    return Response({'error': 'Audio file not found in the request.'}, status=400)

                audio_file = request.FILES['audio_file']

                audio = AudioSegment.from_mp3(io.BytesIO(audio_file.read()))
                compressed_audio = audio.export(format='mp3', bitrate='64k')

                category_name = request.data.get('category')
                category, created = Category.objects.get_or_create(name=category_name)

                music_instance = Music(
                    name_music = request.data.get('name_music'),
                    audio_file=ContentFile(compressed_audio.read(), name='audio.mp3'),  
                    image_music = request.data.get('image_music') if 'image_music' in request.data else '/music/defaul_image/sEZB30zciy5YEGCrSUPkhKNMjcXUm7YdvC0PwpwIYZ3CRmhrXUDBnGwbKnN-ya9Z4VSnrqwe.jpg',
                    author=request.user,  
                    category=category,  
                    in_albums=None
                )
                music_instance.save()

                return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=500)























#Get in Postman
class MusicOutputView(viewsets.ViewSet):
    def list(self, request):
        try:
            music_objects = Music.objects.all()

            serializer = MusicOutputSerializer1(music_objects, many=True)
            data = serializer.data
            for item in data:
                music_id = item.get('id')
                likes_count = Like.objects.filter(music__id=music_id).count()
                item['likes_count'] = likes_count
                logging.debug('Это сообщение отладочного уровня')
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(['POST', 'DELETE'], detail=True)
    def like(self, request, pk):
        music = get_object_or_404(Music, pk=pk)
        user = request.user
        if user.is_authenticated:
            if request.method == 'POST':
                if user.likes.filter(music=music).exists():
                    return Response({'detail': 'This music has already been liked'}, status=status.HTTP_201_CREATED)
                Like.objects.create(owner=user, music=music)
                logging.debug('Это сообщение отладочного уровня')
                return Response({'detail': 'You have liked this music'}, status=status.HTTP_201_CREATED)

            elif request.method == 'DELETE':
                likes = user.likes.filter(music=music)
                if likes.exists():
                    likes.delete()
                    logging.debug('Это сообщение отладочного уровня')
                    return Response({'detail': 'Like has been deleted'}, status=status.HTTP_204_NO_CONTENT)
                return Response({'detail': 'Music not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'detail': 'You need to be authenticated to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(['GET'], detail=True)
    def get_likes(self, request, pk):
        music = get_object_or_404(Music, pk=pk)
        likes = music.likes.all()
        serializer = LikeSerializer(instance=likes, many=True)
        logging.debug('Это сообщение отладочного уровня')
        return Response(serializer.data, status=status.HTTP_200_OK)


class MusicDetailView(DestroyAPIView):
    queryset = Music.objects.all()
    serializer_class = MusicOutputSerializer1
    lookup_field = 'pk' 
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

































#Get visual data in HTML.CSS
def music_website(request):
    music_data = Music.objects.all()
    album_data = Albums.objects.all()
    category_data = Category.objects.all()
    return render(request, 'music_website.html', {'music_data': music_data, 'album_data': album_data,'category_data':category_data})


from django.shortcuts import render
from .models import Music, Category

def sort_website(request):
    name_param = request.GET.get('name', '')

    if name_param:
        sort_music = Music.objects.filter(category__name=name_param)
        return render(request, 'sorted_music.html', {'music_data': sort_music})
    else:
        return redirect('music_website.html')


from django.shortcuts import render
from .models import Music

def filter_music_by_album(request):
    templates_name = 'album.html'
    title_param = request.GET.get('name', '')

    if title_param:
        filtered_music = Music.objects.filter(in_albums__title=title_param)
        filtered_album = Albums.objects.filter(title= title_param)
        str(filtered_album)
        print(filtered_album)
        return render(request, templates_name, {'music_data': filtered_music,'album_data':filtered_album})
    else:
        return redirect('music_website')
