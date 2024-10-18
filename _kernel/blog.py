from _kernel.util import Util
import os, re, jieba

class Blog:
    def __init__(self, title = None, author = None, date = None, description = None, 
                 type_ = None, language = None, category = None, categories = None, 
                 target_file_path = None, ps = None, redirect = None, gen_file_path = None,
                 pri_category = None):
        self.title = title
        self.author = author
        self.date = date
        self.description = description
        self.type_ = type_
        self.language = language
        self.category = category
        self.target_file_path = target_file_path
        self.gen_file_path = gen_file_path
        self.ps = ps
        self.redirect = redirect
        self.categories = categories
        self.pri_category = pri_category

        self.date_year, self.date_month, self.date_day = self._split_date()
        self.content = None
        self._keywords = None
        self.scale   = 1

    def generate(self):
        with open(self.target_file_path, 'r') as f:
            content = f.read()
            return Util.markdown_to_html(content, 
                    {'pic_path': Util.calculate_relative_path(self.gen_file_path, os.path.dirname(self.target_file_path))})
        return

    @property
    def keywords(self):
        if self._keywords is not None:
            return self._keywords
        
        def read_file(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return content

        def remove_header(content):
            pattern = r'^---\n.*?\n---\n'
            return re.sub(pattern, '', content, flags=re.DOTALL)

        def load_stopwords(stopwords_file):
            with open(stopwords_file, 'r', encoding='utf-8') as file:
                return set(line.strip() for line in file)

        def generate_vocabulary(text, stopwords):
            words = jieba.lcut(text)
            return [word for word in words if word not in stopwords and word.strip()]

        def format_vocabulary(vocabulary):
            return ', '.join(f'"{word}"' for word in vocabulary)

        def process_file(file_path, stopwords_file):
            content = read_file(file_path)
            content = remove_header(content)
            stopwords = load_stopwords(stopwords_file)
            vocabulary = generate_vocabulary(content, stopwords)
            self.scale = len(vocabulary)
            formatted_vocabulary = format_vocabulary(vocabulary)
            return formatted_vocabulary
        
        self._keywords = process_file(self.target_file_path, "./_kernel/stopwords.txt")
        return self._keywords
    
    def _split_date(self):
        year, month, day = map(int, self.date.split('-'))
        return year, month, day

    def __repr__(self):
        return f"\nBlog(title='{self.title}',\nauthor='{self.author}',\ndate='{self.date}',\n" \
               f"description='{self.description}',\n" \
               f"type='{self.type_}', language='{self.language}', category='{self.category}',\n" \
               f"target_file_path='{self.target_file_path}',\n" \
               f"gen_file_path='{self.gen_file_path}',\n" \
               f"ps='{self.ps}',\n" \
               f"redirect='{self.redirect}'\n)"