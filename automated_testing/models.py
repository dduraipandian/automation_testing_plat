import re
from django.db import models
from django.utils.text import slugify
from django.utils.html import mark_safe
from users.utils import get_user_model
from bs4 import BeautifulSoup


def directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/{1}'.format(instance.title.id, filename)


# Create your models here.
class Article(models.Model):
    Author = get_user_model()
    HEADER_CHOICES = [(h, h) for h in ['H1', 'H2', 'H3', 'H4', 'H5']]
    STATUS_CHOICES = [(h, h) for h in ['DRAFT', 'PUBLISHED']]

    title = models.CharField(max_length=200, unique=True)
    slug_title = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to=directory_path, null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='blog_author')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    header_choice = models.CharField(max_length=5, choices=HEADER_CHOICES, default='h3')

    def image_tag(self):
        img = None
        if self.image:
            img = mark_safe(
                f'<img src="{self.image.url}" alt="{self.title}" width="30" height="30" style="object-fit: cover;"/>')
        return img

    image_tag.short_description = 'Image'

    def author_name(self):
        return self.author.name

    def save(self, *args, **kwargs):
        if not self.slug_title:
            self.slug_title = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class ArticleContent(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name="article_content")
    content = models.TextField()
    toc = models.TextField(null=True, blank=True)

    def get_toc(self):
        toc = None
        content = self.content
        soup = BeautifulSoup(content, 'html.parser')

        if content:
            header_choice = self.article.header_choice
            if not header_choice:
                header_choice = "H1"
            header_choice = header_choice[-1]
            re_c = f"^h[{header_choice}-{header_choice}]"

            toc = ""
            for tag in soup.find_all(re.compile(re_c)):
                heading = tag.text.strip()
                slug_id = slugify(heading)
                toc = toc + f"<li class='toc_li'><a href='#{slug_id}'>{heading}</a></li>"
                tag['id'] = slug_id

            if toc:
                toc = f"<ul class='toc_ul'>{toc}</ul>"

        return toc, str(soup)

    def save(self, *args, **kwargs):
        self.toc, self.content = self.get_toc()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.article.title
