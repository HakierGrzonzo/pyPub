import ebooklib, json
from ebooklib import epub
from pprint import pprint as pp

class Book():
    def __init__(self, book_filepath):
        super(Book, self).__init__()
        try:
            self.book = epub.read_epub(book_filepath)
        except:
            raise FileNotFoundError()
        self.content_spine_ids = [x[0] for x in self.book.spine]
        self.id_to_href = dict()
        for item in self.book.get_items():
            self.id_to_href[item.get_id()] = item.get_name()
    def is_valid_chapter(self, num):
        if num in range(len(self.content_spine_ids)):
            return True
        else:
            return False
    def get_href(self, href):
        item = self.book.get_item_with_href(href)
        return item
    def get_title(self):
        return self.book.get_metadata('DC', 'title')[0][0]
