from django.test import TestCase
from django.contrib.auth.models import User
from .models import Posts,Profile,Comments,Likes,Follow
# Create your tests here.



class UserTest(TestCase):
    def setUp(self):
        self.user=User(username='dk',first_name='d',last_name='k',email='dk@gmail.com')
    
    def test_instance(self):
        self.assertTrue(isinstance(self.user,User))
    
    def test_data(self):
        self.assertTrue(self.user.username,"dk")
        self.assertTrue(self.user.first_name,"d")
        self.assertTrue(self.user.last_name,'k')
        self.assertTrue(self.user.email,'dk@gmail.com')
    
    def test_save(self):
        self.user.save()
        users = User.objects.all()
        self.assertTrue(len(users)>0)
    
    def test_delete(self):
        user = User.objects.filter(id=1)
        user.delete()
        users = User.objects.all()
        self.assertTrue(len(users)==0)

class ProfileTest(TestCase):
    def setUp(self):
        self.new_user=User(username='aa',first_name='a',last_name='a',email='a@gmail.com')
        self.new_user.save()
        self.new_profile=Profile(user=self.new_user,bio='wueh')

    def test_instance(self):
        self.assertTrue(isinstance(self.new_profile,Profile))
    
    def test_data(self):
        self.assertTrue(self.new_profile.bio,"wuehh")
        self.assertTrue(self.new_profile.user,self.new_user)

    def test_save(self):
        self.new_profile.save()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles)>0)
    
    def test_delete(self):
        profile = Profile.objects.filter(id=1)
        profile.delete()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles)==0)

    
    def test_edit_profile(self):
        self.new_profile.save()
        self.update_profile = Profile.objects.filter(bio='wueh').update(bio = 'aaabbbcccddd')
        self.updated_profile = Profile.objects.get(bio='aaabbbcccddd')
        self.assertTrue(self.updated_profile.bio,'aaabbbcccddd')



class postsTest(TestCase):
    def setUp(self):
        self.user=User(username='dk',first_name='d',last_name='k',email='dk@gmail.com')
        self.user.save()
        self.new_profile=Profile(user=self.user,bio='wueh')
        self.new_profile.save()
        self.new_post = Posts(user=self.user,caption="eating",profile=self.new_profile)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_post,Posts))
    
    def test_data(self):
        self.assertTrue(self.new_post.caption,"eating")
        
    def test_save(self):
        self.new_post.save()
        posts = Posts.objects.all()
        self.assertTrue(len(posts)>0)
    
    def test_delete(self):
        post = Posts.objects.filter(id=1)
        post.delete()
        posts = Posts.objects.all()
        self.assertTrue(len(posts)==0)

    def test_update_post(self):
        self.new_post.save()
        self.update_post = Posts.objects.filter(caption='eating').update(caption = 'aaabbbcccddd')
        self.updated_post = Posts.objects.get(caption='aaabbbcccddd')
        self.assertTrue(self.updated_post.caption,'aaabbbcccddd')


class LikeTest(TestCase):
    def setUp(self):
        self.user=User(username='dk',first_name='d',last_name='k',email='dk@gmail.com')
        self.user.save()
        self.new_profile=Profile(user=self.user,bio='wueh')
        self.new_profile.save()
        self.new_post = Posts(user=self.user,caption="eating",profile=self.new_profile)
        self.new_post.save()
        self.like=Likes(user=self.user,post=self.new_post)
    
    def test_likes(self):
        self.like.save()
        likes=Likes.objects.all()
        self.assertTrue(len(likes)>0)

class CommentTest(TestCase):
    def setUp(self):
        self.new_user=User(username='aa',first_name='a',last_name='a',email='a@gmail.com')
        self.new_user.save()
        self.new_profile=Profile(user=self.new_user,bio='wueh')
        self.new_profile.save()
        self.new_post = Posts(user=self.new_user,caption="eating",profile=self.new_profile)
        self.new_post.save()
        self.comment=Comments(user=self.new_user,post=self.new_post,comment='good')

    def test_instance(self):
        self.assertTrue(isinstance(self.comment,Comments))

    def test_data(self):
        self.assertTrue(self.comment.comment,"good")

    def test_comments(self):
        self.comment.save()
        comments=Comments.objects.all()
        self.assertTrue(len(comments)>0)

        



    