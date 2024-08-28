import factory
from django.utils.text import slugify
from datetime import timezone

from sage_blog.models import PostCategory, PostTag, Post, PostFaq

class PostCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PostCategory

    title = factory.Faker('word')
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))
    is_published = factory.Faker('boolean', chance_of_getting_true=75)

class PostTagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PostTag

    title = factory.Faker('word')
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))
    is_published = factory.Faker('boolean', chance_of_getting_true=75)

class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Faker('sentence', nb_words=6)
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))
    summary = factory.Faker('sentence', nb_words=12)
    description = factory.Faker('text', max_nb_chars=200)
    is_published = factory.Faker('boolean', chance_of_getting_true=75)
    published_at = factory.Faker('date_time_this_decade', before_now=True, tzinfo=timezone.utc)
    category = factory.SubFactory(PostCategoryFactory)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        
        if extracted:
            for tag in extracted:
                self.tags.add(tag)

class PostFaqFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PostFaq
    
    question = factory.Faker('sentence', nb_words=10)
    answer = factory.Faker('paragraph', nb_sentences=3)
    post = factory.SubFactory(PostFactory)
