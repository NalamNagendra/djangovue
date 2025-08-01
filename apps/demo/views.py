import random
from django.db.models import Count
from rest_framework.response import Response
from rest_framework import generics, serializers
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['text', 'timestamp', 'author']

    def get_author(self, obj):
        return obj.user.username


class PostSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['text', 'timestamp', 'comment_count', 'comments', 'author']

    def get_comment_count(self, obj):
        return obj.comment_count if hasattr(obj, 'comment_count') else obj.comment_set.count()

    def get_comments(self, obj):
        
        comments = obj.comment_set.all()
        
        
        request = self.context.get('request')
        if request and request.query_params.get('random', '').lower() == 'true':
            
            comment_count = comments.count()
            if comment_count <= 3:
                
                comments = list(comments)
            else:
                
                comments = list(comments.order_by('?')[:3])
            
            comments = sorted(comments, key=lambda x: x.timestamp, reverse=True)
        else:
            
            comments = comments.order_by('-timestamp')[:3]
        
        serializer = CommentSerializer(comments, many=True)
        return serializer.data
    
    def get_author(self, obj):
        return obj.user.username


class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    
    def get_queryset(self):
        
        return Post.objects.select_related('user')\
                         .prefetch_related('comment_set__user')\
                         .annotate(comment_count=Count('comment_set'))\
                         .order_by('-timestamp')

    def list(self, request):
        try:
            queryset = self.get_queryset()
            
            
            page = request.query_params.get('page', 1)
            paginator = Paginator(queryset, 10) 

            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)

            serializer = self.get_serializer(posts, many=True, context={'request': request})
            
            return Response({
                'posts': serializer.data,
                'num_pages': paginator.num_pages,
                'current_page': int(page),
                'has_next': posts.has_next()
            })
        except Exception as e:
            print(f"Error in PostListView: {str(e)}")  
            return Response(
                {"error": "An error occurred while processing your request."},
                status=500
            )