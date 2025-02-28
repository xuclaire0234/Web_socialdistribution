# 2023-02-13
# post/models.py
# For ERD refer here: https://github.com/CMPUT-404-2023-Not-Found/CMPUT404-project-socialdistribution/wiki/ERD

from django.conf import settings
from django.db import models

from author.models import Author
from utils.model_abstracts import Model

class Post(Model):
    MD = 'text/markdown';       PT = 'text/plain'
    B64 = 'application/base64'; PNG = 'image/png;base64'; JPEG = 'image/jpeg;base64'
    CONTENT_TYPE_OPTIONS = [
        (MD,    'Markdown'),
        (PT,    'Plain Text'),
        (B64,   'Base64'),
        (PNG,   'PNG Image'),
        (JPEG,  'JPEG Image'),
    ]
    PUB = 'PUBLIC'; FRI = 'FRIENDS'
    VISIBILITY_OPTIONS = [
        (FRI, 'Friends'),
        (PUB, 'Public')
    ]
    
    # Identification fields
    author              = models.ForeignKey(to=Author, on_delete=models.CASCADE, verbose_name="Owner's Author Id")
    host                = models.URLField(default=settings.APP_URL, max_length=128, help_text='The node that created the post')

    # Modification fields
    published           = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Published At')
    updated_at          = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Last Updated At')
    rev                 = models.IntegerField(default=0)

    # Access fields
    unlisted            = models.BooleanField(default=False, help_text='Does this post appear in authors streams')
    visibility          = models.CharField(choices=VISIBILITY_OPTIONS, max_length=16, help_text='Who can view this post')

    # Origin fields
    origin              = models.URLField(default=settings.APP_URL, max_length=128, help_text='The node that created the post')
    source              = models.URLField(default=settings.APP_URL, max_length=128, help_text='The node that shared the post')

    # Content fields
    # categories ... this will be tricky because we need to have multiple string values ... thus another model will link to post
    #   ignore categories for now
    content             = models.TextField(blank=False, null=False)
    content_type        = models.CharField(choices=CONTENT_TYPE_OPTIONS, max_length=32, verbose_name='Content Type')
    description         = models.TextField(blank=True, default='')
    title               = models.CharField(blank=False, null=False, max_length=128)
    def __str__(self):
        return f'{self.author} {self.title}'

    def get_node_id(self):
        return f'{self.author.get_node_id()}/posts/{self.id}'

    def get_category_item_list(self):
        return self.category_set.values_list('category', flat=True)

class Category(models.Model):
    id                 = models.AutoField(primary_key=True)
    category           = models.CharField(max_length=128, null=True, blank=True, default="post")
    post               = models.ForeignKey(to=Post, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.category}'
    
    class Meta:
        verbose_name_plural = 'Categories'
    
