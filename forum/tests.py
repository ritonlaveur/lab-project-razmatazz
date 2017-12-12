from django.test import TestCase

# Create your tests here.

from .models import Post

from django.utils import timezone

# class ForumViewsTestCase(TestCase):
#     def text_index(self):
#         resp = self.client.get('/')
#         self.assertEqual(resp.status_code,200)

class PostTestCase(TestCase):
    def setUp(self):
        Post.objects.create(title="Post1",text="This is Post1",date=timezone.now(),author="Shakeel")
        Post.objects.create(title="Post2",text="This is Post2",date=timezone.now(),author="Tabia")

    def test_posts_created(self):
        post1 = Post.objects.get(title="Post1")
        post2 = Post.objects.get(title="Post2")
        self.assertEqual(post1.__str__(),"Post1")
        self.assertEqual(post2.__str__(),"Post2")
        
    def test_posts_text(self):
        post1 = Post.objects.get(title="Post1")
        post2 = Post.objects.get(title="Post2")
        self.assertEquals(post1.text,"This is Post1")
        self.assertEquals(post2.text,"This is Post2")
