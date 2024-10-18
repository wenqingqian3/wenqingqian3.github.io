import os, re
from _kernel.blog import Blog
from _kernel.util import Util, AdaptiveScaler

class Engine:

    def __init__(self, config):
        self.config = config
        self.BLOGMD = self.config['BLOG']['PATH']['MD']
        self.BLOGWEB = self.config['BLOG']['PATH']['WEB']
        self.BLOGONLINE = self.config['BLOG']['PATH']['ONLINE']
        self.BLOGREDIRECT = self.config['BLOG']['PATH']['REDIRECT']
        self.BLOG_INDEX_PATH = self.config["BLOG"]["PATH"]["INDEX"]
        
        self.DOWNLOAD_PAGE = self.config['DOWNLOAD']['PATH']['INDEX']
        self.DOWNLOAD_DIR  = self.config['DOWNLOAD']['PATH']['RESOURCE']

        self.HOMEPAGE = self.config["HOME"]["PATH"]
        
        self.blogs : list[Blog] = []

    def start(self):
        self._quick_fix()

        self._gen_home_page()
        self._gen_download_page()

        self._parse_blog()
        # must do this before gen
        self._gen_search_metadata()
        self._gen_blog_index()
        self._gen_blog()


    def _gen_home_page(self):

        with open("./_kernel/html-template/index.html") as f:
            content = f.read()
        RELATIVE_PATH_TO_RENDER   = Util.calculate_relative_path(self.HOMEPAGE, './render')  
        RELATIVE_PATH_TO_HOME     = Util.calculate_relative_path(self.HOMEPAGE, './webroot/index.html')
        RELATIVE_PATH_TO_RESUME   = Util.calculate_relative_path(self.HOMEPAGE, self.config["RESUME"]["PATH"])
        RELATIVE_PATH_TO_NOTE     = Util.calculate_relative_path(self.HOMEPAGE, self.BLOG_INDEX_PATH)
        RELATIVE_PATH_TO_DOWNLOAD = Util.calculate_relative_path(self.HOMEPAGE, self.DOWNLOAD_PAGE)
        RELATIVE_PATH_TO_OTHER    = Util.calculate_relative_path(self.HOMEPAGE, self.config["OTHER"]["PATH"])

        replacements_gen = {
            'RELATIVE_PATH_TO_RENDER'  : RELATIVE_PATH_TO_RENDER,
            'RELATIVE_PATH_TO_HOME'    : RELATIVE_PATH_TO_HOME,
            'ABOUTME'                  : "</p><p>".join(self.config["HOME"]["about_me"]),
            'ABOUTWEBSITE'             : "</p><p>".join(self.config["HOME"]["about_website"]),
            'NAME'                     : self.config["HOME"]["name"],
            'EMAIL'                    : self.config["HOME"]["email"],
            'GITHUB'                   : self.config["HOME"]["github"],
            'X'                        : self.config["HOME"]["x"],
            'RELATIVE_PATH_TO_RESUME'  : RELATIVE_PATH_TO_RESUME,
            'RELATIVE_PATH_TO_NOTE'    : RELATIVE_PATH_TO_NOTE,
            'RELATIVE_PATH_TO_DOWNLOAD': RELATIVE_PATH_TO_DOWNLOAD,
            'RELATIVE_PATH_TO_OTHER'   : RELATIVE_PATH_TO_OTHER
        }
        
        try:
            new_content = self._replace_autogen(content, replacements_gen)
        except KeyError as e:
            Util.print_error(f'{e}')
            return

        with open(self.HOMEPAGE, 'w') as file:
            file.write(new_content)

    def _gen_download_page(self):
        with open("./_kernel/html-template/download.html") as f:
            content = f.read()
        RELATIVE_PATH_TO_RENDER = Util.calculate_relative_path(self.DOWNLOAD_PAGE, './render')
        # TODO make home movable
        RELATIVE_PATH_TO_HOME   = Util.calculate_relative_path(self.DOWNLOAD_PAGE, './webroot/index.html')

        DOWNLOAD_CONTENT = self._gen_download_content()

        replacements_gen = {
            'RELATIVE_PATH_TO_RENDER': RELATIVE_PATH_TO_RENDER,
            'RELATIVE_PATH_TO_HOME'  : RELATIVE_PATH_TO_HOME,
            'DOWNLOAD_CONTENT'       : DOWNLOAD_CONTENT,
        }
        
        try:
            new_content = self._replace_autogen(content, replacements_gen)
        except KeyError as e:
            Util.print_error(f'{e}')
            return

        with open(self.DOWNLOAD_PAGE, 'w') as file:
            file.write(new_content)

    def _parse_blog(self):
        # parse all markdown
        multi_cate_once_gen = set()
        for blog_cate in os.listdir(self.BLOGMD):
            blog_cate_path = os.path.join(self.BLOGMD, blog_cate)
            if os.path.isdir(blog_cate_path):
                blog_cate_only = os.path.basename(blog_cate_path)
                # Create the corresponding BLOG_WEB directory
                blog_web_cate_path = os.path.join(self.BLOGWEB, blog_cate_only)
                if not os.path.exists(blog_web_cate_path):
                    os.makedirs(blog_web_cate_path)
                for file in os.listdir(blog_cate_path):
                    if file.endswith(".md"):
                        filepath = os.path.join(blog_cate_path, file)
                        filename = os.path.splitext(file)[0]
                        webfilepath = os.path.join(blog_web_cate_path, f'{filename}.html')
                        struct_name = ''.join([c if c.isalnum() else '_' for c in filename])

                        # Parse YAML front matter
                        with open(filepath, "r") as md_file:
                            lines = md_file.readlines()
                            yaml_content = [line.strip() for line in lines if "---" not in line]
                        
                        def get_field(field):
                            return next((line.split(":")[1].strip() for line in yaml_content if line.startswith(field)), "")

                        title = get_field("title")
                        date = get_field("date")
                        description = get_field("description")
                        category = get_field("category")
                        categories = []
                        if category : 
                            categories = category.split()
                        
                        author = get_field("author")
                        type_ = get_field("type")
                        language = get_field("language")
                        ps = get_field("ps")
                        redirect = get_field("redirect")

                        if category and blog_cate_only not in categories:
                            Util.print_warning(f"blog {file} category in file ({category}) \
                                    doesn't match its directory name ({blog_cate_only}).")
                        
                        if len(categories) > 1:
                            if not multi_cate_once_gen.__contains__(f"{struct_name}{category}{title}"):
                                multi_cate_once_gen.add(f"{struct_name}{category}{title}")
                            else:
                                Util.print_error(f"file {blog_cate_only}/{filename}.md exist in other cate in {category}") 
                                continue

                        self.blogs.append(Blog(title=title, date=date, description=description, 
                                        category=category, categories=categories,
                                        pri_category=blog_cate_only, author=author, 
                                        type_=type_, language=language, ps=ps, redirect=redirect, 
                                        target_file_path=filepath, gen_file_path=webfilepath))
        
        # Traverse data in the BLOG_ONLINE directory
        import yaml
        with open(self.BLOGONLINE+'_autogen_row_online_metadata.txt', 'w') as metadata:
            with open(self.BLOGONLINE+'online_metadata.yml', 'r') as file:
                data = yaml.safe_load(file)
                if data is not None: 
                    for entry in data:
                        metadata.write(f'{entry["title"]}\t{entry["cate"]}\t{entry["author"]}\t{entry["platform"]}\t{entry["date"]}\t{entry["link"]}\t{entry["note"]}\n')
                        if not Util.is_none(entry['note']):
                            self.blogs.append(Blog(title=entry["title"], date=f'{entry["date"]}', 
                                            category=entry["cate"], categories=entry["cate"].split(), 
                                            author=entry["author"], type_="online", 
                                            ps=f'@{entry["author"]}-{entry["platform"]}, <a class=\"html\" href=\"./blog/_/{entry["note"]}.html\">note</a>', 
                                            redirect=entry["link"], 
                                            target_file_path=f'{self.BLOGONLINE}/note/{entry["note"]}.md',
                                            gen_file_path=os.path.join(self.BLOGWEB, f'_/{entry["note"]}.html')))
                        else:
                            self.blogs.append(Blog(title=entry["title"], date=f'{entry["date"]}', 
                                            category=entry["cate"], categories=entry["cate"].split(), 
                                            author=entry["author"], type_="online", 
                                            ps=f'@{entry["author"]}-{entry["platform"]}', 
                                            redirect=entry["link"], target_file_path=entry["note"]))
        Util.print_debug(self.blogs)
    
    def _gen_search_metadata(self):
        with open("./_kernel/html-template/search_metadata.txt", 'w') as meta:
            length = []
            for blog in self.blogs:
                if blog.type_ == "online":
                    if not Util.is_none(blog.gen_file_path):
                        blog.keywords
                    else: continue
                elif not Util.is_none(blog.redirect):
                    continue
                else:
                    blog.keywords
                length.append(blog.scale)
            scaler = AdaptiveScaler(1, 5)
            scaler.fit(length)



            for blog in self.blogs:
                meta.write(f'{{')
                meta.write(f'title: "{blog.title}",\n')
                meta.write(f'date: "{blog.date}",\n')
                meta.write(f'type: "{blog.type_}",\n')
                meta.write(f'category: "{blog.category}",\n')
                if blog.type_ == "online":
                    meta.write(f'url: "{blog.redirect}",\n')
                    meta.write(f'author: "{blog.author}",\n')
                    if Util.is_none(blog.gen_file_path):
                        meta.write(f'keywords: [],\n')
                    else:
                        meta.write(f'note: "{{AUTOGEN:RELATIVE_PATH_TO_GEN_FILE_PATH}}/_/{os.path.basename(blog.gen_file_path)}",\n')
                        meta.write(f'keywords: [{blog.keywords}],\n')
                elif not Util.is_none(blog.redirect):
                    meta.write(f'url: "{{AUTOGEN:RELATIVE_PATH_TO_REDIRECT_FILE}}/{blog.redirect}",\n')
                    meta.write(f'keywords: [],\n')
                else:
                    meta.write(f'url: "{{AUTOGEN:RELATIVE_PATH_TO_GEN_FILE_PATH}}/{blog.pri_category}/{os.path.basename(blog.gen_file_path)}",\n')
                    meta.write(f'keywords: [{blog.keywords}],\n')
                meta.write(f'scale: {6 - scaler.transform(blog.scale)},\n')
                meta.write(f'}},\n')


    def _gen_blog_index(self):
        
        if self.config["BLOG"]["INDEX"]["TOC"]:
            # TODO make template movable
            with open("_kernel/html-template/blog_index_with_toc.html", 'r') as f:
                content = f.read()
        else:
            with open("_kernel/html-template/blog_index.html", 'r') as f:
                content = f.read()
        
        # TODO make render movable
        RELATIVE_PATH_TO_RENDER = Util.calculate_relative_path(self.BLOG_INDEX_PATH, './render')
        # TODO make home movable
        RELATIVE_PATH_TO_HOME   = Util.calculate_relative_path(self.BLOG_INDEX_PATH, './webroot/index.html')
        BLOG_INDEX_HEADER       = self.config["BLOG"]["INDEX"]["header"]
        BLOG_INDEX_DESCRIPTION  = self.config["BLOG"]["INDEX"]["description"]
        BLOG_INDEX_TOC,\
        BLOG_INDEX_TOC_MAP,\
        BLOG_INDEX_CONTENT      = self._gen_index_content(self.config["BLOG"]["INDEX"]["TOC"])

        BLOG_SEARCH_METADATA    = self._gen_index_search_metadata()

        replacements_set = {
            'BLOG_INDEX_HEADER'      : BLOG_INDEX_HEADER,
            'BLOG_INDEX_DESCRIPTION' : BLOG_INDEX_DESCRIPTION,
        }
        replacements_gen = {
            'RELATIVE_PATH_TO_RENDER': RELATIVE_PATH_TO_RENDER,
            'BLOG_INDEX_CONTENT'     : BLOG_INDEX_CONTENT,
            'RELATIVE_PATH_TO_HOME'  : RELATIVE_PATH_TO_HOME,
            'BLOG_INDEX_TOC'         : BLOG_INDEX_TOC,
            'BLOG_INDEX_TOC_MAP'     : BLOG_INDEX_TOC_MAP,
            'BLOG_SEARCH_METADATA'   : BLOG_SEARCH_METADATA
        }
        
        try:
            new_content = self._replace_autogen(content, replacements_gen)
            new_content = self._replace_autoset(new_content, replacements_set)
        except KeyError as e:
            Util.print_error(f'{e}')
            return

        with open(self.BLOG_INDEX_PATH, 'w') as file:
            file.write(new_content)

    def _gen_blog(self):
        with open("_kernel/html-template/blog.html", 'r') as f:
            content = f.read()

        BLOG_SEARCH_METADATA    = self._gen_blog_search_metadata()

        for blog in self.blogs:
            if not Util.is_none(blog.redirect):
                if blog.type_ != "online": continue
                elif Util.is_none(blog.gen_file_path): continue

            # TODO make render movable
            RELATIVE_PATH_TO_RENDER = Util.calculate_relative_path(blog.gen_file_path, './render')
            # TODO make home movable
            RELATIVE_PATH_TO_HOME   = Util.calculate_relative_path(blog.gen_file_path, './webroot/index.html')
            RELATIVE_PATH_TO_BLOG_INDEX = Util.calculate_relative_path(blog.gen_file_path, self.BLOG_INDEX_PATH)


            BLOG_TOC,\
            BLOG_TOC_MAP,\
            BLOG_CONTENT  = blog.generate()

            replacements_set = {
                'BLOG_LANGUAGE' : blog.language if not Util.is_none(blog.language) else "chinese",
                'BLOG_HEADER'   : blog.title,
                'BLOG_DATE'     : blog.date
            }
            replacements_gen = {
                'RELATIVE_PATH_TO_RENDER': RELATIVE_PATH_TO_RENDER,
                'RELATIVE_PATH_TO_HOME'  : RELATIVE_PATH_TO_HOME,
                'RELATIVE_PATH_TO_BLOG_INDEX' :RELATIVE_PATH_TO_BLOG_INDEX,
                'BLOG_TOC': BLOG_TOC,
                'BLOG_TOC_MAP':BLOG_TOC_MAP,
                'BLOG_DESCRIPTION' : f'<p>{blog.description}</p>' \
                                    if not Util.is_none(blog.description)\
                                    else "",
                'BLOG_CONTENT':BLOG_CONTENT,
                'BLOG_SEARCH_METADATA': BLOG_SEARCH_METADATA
            }
            try:
                new_content = self._replace_autogen(content, replacements_gen)
                new_content = self._replace_autoset(new_content, replacements_set)
            except KeyError as e:
                Util.print_error(f'{e}')
                return
            with open(blog.gen_file_path, 'w') as f:
                f.write(new_content)

    def _replace_autogen(self, content, replacements):
        pattern = r'\{AUTOGEN:(.*?)\}'
    
        def replacer(match):
            key = match.group(1)
            if key not in replacements:
                raise KeyError(f"Replacement key '{key}' not found in the replacements dictionary.")
            return replacements[key]
        
        return re.sub(pattern, replacer, content)
    
    def _replace_autoset(self, content, replacements):
        pattern = r'\{AUTOSET:(.*?)\}'
        
        def replacer(match):
            key = match.group(1)
            if key not in replacements:
                raise KeyError(f"Replacement key '{key}' not found in the replacements dictionary.")
            return replacements[key]
        
        return re.sub(pattern, replacer, content)
    
    def _gen_index_content(self, toc_flag):
        categories = set()

        for blog in self.blogs:
            categories.update(blog.categories)
        
        self.blogs.sort(key=lambda blog: (blog.date_year, blog.date_month, blog.date_day), reverse=True)

        content = str()

        if not toc_flag:
            for cate in sorted(categories):
                content += f"<section><h1>{Util.convert_udl_to_space(cate)}</h1><ul>\n"
                for blog in self.blogs:
                    try:
                        if cate in blog.categories:
                            is_redirect = not Util.is_none(blog.redirect)
                            is_online = (blog.type_ == "online")
                            href_class = "class=\"online\"" if is_redirect and is_online else \
                                        "class=\"assets\"" if is_redirect else "class=\"html\""
                            # TODO: make redirect-page movable
                            path = blog.redirect if is_redirect and is_online else \
                                (f"./assets/redirect-page/{blog.redirect}" if is_redirect else \
                                f"{Util.calculate_relative_path(self.BLOG_INDEX_PATH, blog.gen_file_path)}")

                            
                            content += f"<li><a {href_class} href=\"{path}\">{blog.title}</a> ( {blog.date}, {blog.type_}"
                            if not Util.is_none(blog.ps):
                                content += f", {blog.ps}"
                            content += " )"
                            if not Util.is_none(blog.description):
                                content += f"<p style=\"color:#adafb1;\">{blog.description}</p>"
                            content += "</li>\n"
                    except RuntimeError:
                        Util.print_error(blog)
                content += "</ul></section>\n"
            return None, None, content
        else:
            for cate in sorted(categories):
                content += f"# {Util.convert_udl_to_space(cate)}\n"
                for blog in self.blogs:
                    try:
                        if cate in blog.categories:
                            is_redirect = not Util.is_none(blog.redirect)
                            is_online = (blog.type_ == "online")
                            href_class = "class=\"online\"" if is_redirect and is_online else \
                                        "class=\"assets\"" if is_redirect else "class=\"html\""
                            path = blog.redirect if is_redirect and is_online else \
                                (f"./assets/redirect-page/{blog.redirect}" if is_redirect else \
                                    f"{Util.calculate_relative_path(self.BLOG_INDEX_PATH, blog.gen_file_path)}")

                            content += f"- <a {href_class} href=\"{path}\">{blog.title}</a> ( {blog.date}, {blog.type_}"
                            if not Util.is_none(blog.ps):
                                content += f", {blog.ps}"
                            content += " )\n"
                            if not Util.is_none(blog.description):
                                content += f"  !@#$ {blog.description.lstrip()}\n"
                    except RuntimeError as e:
                        Util.print_error(f'{e}')
                        Util.print_error(f'{blog}')
            return Util.markdown_to_html(content, None)
        
    def _gen_index_search_metadata(self):
        with open("./_kernel/html-template/search_metadata.txt", 'r') as meta:
            content = meta.read()
        RELATIVE_PATH_TO_GEN_FILE_PATH = Util.calculate_relative_path(self.BLOG_INDEX_PATH, self.BLOGWEB)
        RELATIVE_PATH_TO_REDIRECT_FILE = Util.calculate_relative_path(self.BLOG_INDEX_PATH, self.BLOGREDIRECT)
        replacements = {
            'RELATIVE_PATH_TO_GEN_FILE_PATH' : RELATIVE_PATH_TO_GEN_FILE_PATH,
            'RELATIVE_PATH_TO_REDIRECT_FILE' : RELATIVE_PATH_TO_REDIRECT_FILE
        }

        ncontent = self._replace_autogen(content, replacements)
        return ncontent
    
    def _gen_blog_search_metadata(self):
        with open("./_kernel/html-template/search_metadata.txt", 'r') as meta:
            content = meta.read()
        RELATIVE_PATH_TO_GEN_FILE_PATH = Util.calculate_relative_path(self.BLOGWEB+"/_/", self.BLOGWEB)
        RELATIVE_PATH_TO_REDIRECT_FILE = Util.calculate_relative_path(self.BLOGWEB+"/_/", self.BLOGREDIRECT)
        replacements = {
            'RELATIVE_PATH_TO_GEN_FILE_PATH' : RELATIVE_PATH_TO_GEN_FILE_PATH,
            'RELATIVE_PATH_TO_REDIRECT_FILE' : RELATIVE_PATH_TO_REDIRECT_FILE
        }

        ncontent = self._replace_autogen(content, replacements)
        return ncontent
    
    def _gen_download_content(self):        
        new_content = ""
        page2resource = Util.calculate_relative_path(self.DOWNLOAD_PAGE, self.DOWNLOAD_DIR)

        for subdir in os.listdir(self.DOWNLOAD_DIR):
            subdir_path = os.path.join(self.DOWNLOAD_DIR, subdir)
            if os.path.isdir(subdir_path):
                new_content += f'<section>\n\t<h1>{subdir}</h1>\n\t<ul>\n'

                for file in os.listdir(subdir_path):
                    file_path = os.path.join(subdir_path, file)
                    if os.path.isfile(file_path):

                        new_content += f'\t\t<li><a href="{page2resource}/{subdir}/{file}" download>{file}</a></li>\n'

                new_content += '\t</ul>\n</section>\n'
        return new_content
    
    def _quick_fix(self):
        blognote = os.path.join(self.BLOGWEB, '_/')
        if not os.path.exists(blognote):
            os.makedirs(blognote)

