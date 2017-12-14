from __future__ import unicode_literals



from django.db import models



class Post(models.Model):

    title = models.CharField(max_length=200)

    text = models.TextField()

    date = models.DateField(auto_now=True)

    author = models.CharField(max_length=50,default="Anonymous")
    
    def __str__(self):
        return self.title

    

    def __str__(self):

        return self.title



class Comment(models.Model):
<<<<<<< HEAD

    post = models.ForeignKey(Post,on_delete=models.CASCADE,)

    title = models.CharField(max_length=200,default="Comment")

=======
    post = models.ForeignKey(Post,on_delete=models.CASCADE,)
    title = models.CharField(max_length=200,default="Comment")
>>>>>>> ccae6210697fbedb3e5b15e3364a08ee0500fd10
    text = models.TextField()

    date = models.DateField(auto_now=True)
<<<<<<< HEAD

    author = models.CharField(max_length=50,default="Anonymous")
=======
    author = models.CharField(max_length=50,default="Anonymous")
    def __str__(self):
        return self.title
>>>>>>> ccae6210697fbedb3e5b15e3364a08ee0500fd10

    def __str__(self):

        return self.title