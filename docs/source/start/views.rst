View Mixins
===========

Django Sage Blog provides several mixins to enhance the functionality of your views. This documentation will explain how to use `SageBlogContextMixin`, `PaginatedMixin`, and `SearchableMixin` in your views to streamline your development process.

SageBlogContextMixin
--------------------

The `SageBlogContextMixin` enriches your views with additional context data related to blog categories, recent posts, and tags. Here’s a breakdown of its functionality:

``class SageBlogContextMixin`` `Attributes`

.. list-table::
   :header-rows: 1

   * - Attribute
     - Description
     - Default Value
   * - ``categories_context_name``
     - The context variable name for categories.
     - ``"sage_blog_categories"``
   * - ``recent_posts_context_name``
     - The context variable name for recent posts.
     - ``"sage_blog_recent_posts"``
   * - ``tags_context_name``
     - The context variable name for tags.
     - ``"sage_blog_tags"``
   * - ``recent_posts_limit``
     - The number of recent posts to include.
     - 3
   * - ``tags_days_ago``
     - The number of days to look back for trending tags.
     - 0
   * - ``tags_min_count``
     - The minimum number of posts required for a tag to be considered trending.
     - 1
   * - ``tags_limit``
     - The maximum number of tags to include.
     - 5


When you use this mixin in your view, it will automatically add the specified context variables for categories, recent posts, and tags. This is useful for displaying sidebar widgets or other related content on your blog pages.

.. note::

    This mixin is especially useful for enhancing the user experience by providing dynamic and relevant content, such as recent posts and trending tags.

Example usage in a view:

.. code-block:: python

    from django.views.generic import ListView
    from sage_blog.mixins import SageBlogContextMixin
    from sage_blog.models import Post

    # View without additional attributes
    class BlogListView(SageBlogContextMixin, ListView):
        model = Post
        template_name = 'blog/post_list.html'

    # View with additional attributes
    class CustomizedBlogListView(SageBlogContextMixin, ListView):
        model = Post
        template_name = 'blog/post_list.html'
        
        categories_context_name = 'custom_categories'
        recent_posts_context_name = 'custom_recent_posts'
        tags_context_name = 'custom_tags'
        recent_posts_limit = 5
        tags_days_ago = 7
        tags_min_count = 2
        tags_limit = 10


PaginatedMixin
--------------

The `PaginatedMixin` simplifies the implementation of pagination in your views. It reads the `paginate_by` attribute from the Django settings, defaulting to 15 if not set.

To configure the pagination, you can add the `paginate_by` attribute in your `settings.py` file. For example:

.. code-block:: python

    # settings.py
    BLOG_POST_PER_PAGE = 15

Then, in your view, you can retrieve this setting using `getattr`:

.. code-block:: python

    from django.views.generic import ListView
    from sage_blog.mixins import PaginatedMixin
    from django.conf import settings
    from sage_blog.models import Post

    class PaginatedBlogListView(PaginatedMixin, ListView):
        model = Post
        template_name = 'blog/post_list.html'
        paginate_by = getattr(settings, "BLOG_POST_PER_PAGE", 15)

.. important::

    Pagination is essential for improving the user experience on your blog by breaking down content into manageable pages.

SearchableMixin
---------------

The `SearchableMixin` empowers your views with advanced search capabilities, making it easier for users to find the content they need. It extracts the search query parameter from the request and refines the queryset accordingly. When no search query is provided, it utilizes the `PostFilter` class for additional filtering.

- **search_param_name**: The name of the search parameter in the request. Defaults to `"search"`.

This mixin significantly enhances user engagement by streamlining the search process.

Example usage in a view:

.. code-block:: python

    from django.views.generic import ListView
    from sage_blog.mixins import SearchableMixin
    from sage_blog.models import Post

    class SearchableBlogListView(SearchableMixin, ListView):
        model = Post
        template_name = 'blog/post_list.html'

Search Queryset
---------------

The `SearchableMixin` offers a comprehensive search experience by integrating multiple search methodologies. Here's a closer look at how it works:

.. list-table:: Search Methods
   :header-rows: 1

   * - Method
     - Description
     - Efficiency
   * - **Full-Text Search**
     - Targets complete words or phrases within the `title` and `description` fields, providing the most efficient way to find exact matches.
     - High
   * - **Substring Search**
     - Ideal for partial word matches, this method performs a case-insensitive search within the `title` and `description` fields.
     - Moderate
   * - **Trigram Similarity Search**
     - Uses trigram similarity to identify posts that closely match the search query. It supports partial word matches and is more linguistically aware but requires PostgreSQL with the `pg_trgm` extension.
     - Moderate to High

.. note::

    **Combining Search Methods for Optimal Results:**

    1. **Full-Text Search**: Initially, the mixin performs a full-text search. If no matches are found, it moves to the next method.
    2. **Substring Search**: If the full-text search yields no results, the mixin conducts a substring search.
    3. **Trigram Similarity Search**: For databases supporting it, the mixin employs a trigram similarity search for more nuanced matching.

    This layered approach ensures that users can effortlessly find relevant content, even with varied search queries. The mixin adapts to different search needs, enhancing the overall user experience.

.. tip::

    By incorporating `heavy_search`, your views can deliver a powerful search functionality that maximizes content discoverability, boosting user satisfaction and engagement.


Combining Mixins
----------------

You can combine these mixins to create views with enhanced functionality. For example, you can create a view that includes context data, pagination, and search functionality:

.. code-block:: python

    from django.views.generic import ListView
    from sage_blog.mixins import SageBlogContextMixin, PaginatedMixin, SearchableMixin
    from sage_blog.models import Post

    class EnhancedBlogListView(SageBlogContextMixin, PaginatedMixin, SearchableMixin, ListView):
        model = Post
        template_name = 'blog/post_list.html'

.. tip::

    By combining these mixins, you can add powerful features to your Django views with minimal effort, improving the overall functionality and user experience of your blog.

By using these mixins, you can add powerful features to your Django views with minimal effort, improving the overall functionality and user experience of your blog.
