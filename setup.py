from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="django-sage-blog",
    version="0.1.3",
    author="Sepehr Akbarzadeh",
    author_email="info@sageteam.org",
    description="Comprehensive Django package designed to seamlessly integrate blogging capabilities into your Django project.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sageteamorg/django-sage-blog",
    project_urls={
        "Documentation": "https://django-sage-blog.readthedocs.io/en/latest/",
        "Source Code": "https://github.com/sageteamorg/django-sage-blog",
        "Issues": "https://github.com/sageteamorg/django-sage-blog/issues",
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.11",
)
