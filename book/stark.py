from .models import *

from stark.service.sites import site, ModelStark


class BookConfig(ModelStark):
    list_display = ["title", "price", "publisher", "authors"]
    list_display_links = ["title"]
    search_fields = ["title", "price"]
    list_filter = ["publisher", "authors"]


site.register(Book, BookConfig)
site.register(Publish)
site.register(Author)
