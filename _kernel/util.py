from colorama import init, Fore
import re, os


init(autoreset=True)

class H3:
    def __init__(self, name_toc, name_real):
        self.name_toc = name_toc
        self.name_real = name_real

class H2:
    def __init__(self, name_toc, name_real):
        self.name_toc = name_toc
        self.name_real = name_real
        self.h3v = []

class H1:
    def __init__(self, name_toc, name_real):
        self.name_toc = name_toc
        self.name_real = name_real
        self.h2v = []

def unique_toc_name(name, toc_name_set):
    while name in toc_name_set:
        name += "_O_o"
    toc_name_set.add(name)
    return name

def is_number(s):
    return s.isdigit()

class Util:
    DEBUG = False
    @staticmethod
    def print_warning(message):
        print(Fore.YELLOW + "[WARNING] " + message)
    @staticmethod
    def print_error(message):
        print(Fore.RED + "[ERROR] " + message)
    @staticmethod
    def print_info(message):
        print(Fore.GREEN + "[INFO] " + message)
    @staticmethod
    def print_debug(message):
        if Util.DEBUG : print(Fore.BLUE + "[DEBUG] " + f'{message}')
    @staticmethod
    def replace_invalid_chars(s):
        return re.sub(r'[^\w]', 'UNVAILD_TOKEN', s)
    @staticmethod
    def calculate_relative_path(file_path, target_dir):
        if Util.is_none(file_path) or Util.is_none(target_dir):
            raise RuntimeError(f'file-path:{file_path}, target-path:{target_dir}')
        file_dir = os.path.dirname(file_path)
        relative_path = os.path.relpath(target_dir, file_dir)
        return relative_path
    @staticmethod
    def convert_udl_to_space(strs):
        return strs.replace('_', ' ')
    @staticmethod
    def is_none(a):
        return a == "none" or a is None or a.strip() == ""
    @staticmethod
    def replace_chinese_punctuation(text):
        text = text.replace('，', ', ').replace('。', '. ').replace('：', ': ')
        return text
    @staticmethod
    def markdown_to_html(markdown, args):
        markdown = Util.replace_chinese_punctuation(markdown)

        toc_name = set()
        h1v = []
        html = []
        section = []
        in_section = False
        in_math_block = False
        in_list = False
        in_metadata = False
        skip_metadata = False
        math_block = []
        list_item_regex = re.compile(r"^(\s*)-\s+(.*)")
        indent_regex = re.compile(r"^(\s*)(.*)")
        last_indent_level = -1
        indent_count = [0] * 100

        lines = markdown.split('\n')

        for line in lines:
            emptyline = re.sub(r"^\s+|\s+$", "", line)
            if not emptyline:
                continue

            if emptyline == "---":
                if not in_metadata:
                    in_metadata = True
                    skip_metadata = True
                    continue
                else:
                    skip_metadata = False
                    continue

            if skip_metadata:
                continue

            match = list_item_regex.search(line)

            if line and in_list and not list_item_regex.search(line):
                match = indent_regex.search(line)
                indent = match[1]

                if len(indent) == last_indent_level + 2:
                    item = match[2]
                    item = re.sub(r"^\s?\$\$(.*?)\$\$\s?$", r"<div>\[ \1 \]</div>", item)
                    item = re.sub(r"\$(.*?)\$", r"\(\1\)", item)
                    item = re.sub(r"`(.*?)`", r"<code>\1</code>", item)
                    if item.startswith("!@#$"):
                        section.append(f"<p style=\"margin-bottom: 0em;color:#adafb1\">{item[4:]}</p>")
                    else:
                        section.append(f"<p style=\"margin-bottom: 0em;\">{item}</p>")
                    continue
                else:
                    for i in range(100):
                        while indent_count[i] != 0:
                            section.append("</ul>")
                            indent_count[i] -= 1
                    in_list = False
                    last_indent_level = -1

            if not re.match(r"^\$\$", line) and in_math_block:
                math_block.append(line)

            elif re.match(r"^\$\$", line) and not in_math_block:
                in_math_block = True

            elif re.match(r"^\$\$", line) and in_math_block:
                section.append("<div>\\[" + "\\]\\[".join(math_block) + "\\]</div>")
                math_block = []
                in_math_block = False

            elif re.match(r"^# .+", line):
                if in_section:
                    section.append("</section>")
                    html.append("\n".join(section))
                    section = []
                section.append("<section>")
                h1name = unique_toc_name(line[2:], toc_name)
                section.append(f"<h1 id=\"{h1name}\">{line[2:]}</h1>")
                in_section = True
                h1v.append(H1(name_toc=h1name, name_real=line[2:]))

            elif re.match(r"^## .+", line):
                h2name = unique_toc_name(line[3:], toc_name)
                section.append(f"<h2 id=\"{h2name}\">{line[3:]}</h2>")
                if not h1v:
                    Util.print_error("must have h1 before h2")
                h1v[-1].h2v.append(H2(name_toc=h2name, name_real=line[3:]))

            elif re.match(r"^### .+", line):
                h3name = unique_toc_name(line[4:], toc_name)
                section.append(f"<h3 id=\"{h3name}\">{line[4:]}</h3>")
                if not h1v:
                    Util.print_error("must have h1 before h3")
                if not h1v[-1].h2v:
                    Util.print_error("must have h2 before h3")
                h1v[-1].h2v[-1].h3v.append(H3(name_toc=h3name, name_real=line[4:]))

            elif re.match(r"^#### .+", line):
                Util.print_warning("currently not support h4, treat as plain text")
                section.append(f"<p>{line[5:]}</p>")
            elif re.match(r"^##### .+", line):
                Util.print_warning("currently not support h5, treat as plain text")
                section.append(f"<p>{line[6:]}</p>")
            elif re.match(r"^!\[(.+?)\].*", line):
                parts = re.search(r'^!\[(.+?)\]\((.+?)\)(.*)', line)

                sizes = parts.group(1)
                sizev = [s.strip() for s in sizes.split(',')]

                links = parts.group(2)
                linkv = [l.strip() for l in links.split(',')]
                
                descs = parts.group(3)
                desc  = ""
                if re.match(r'^\((.+?)\)', descs):
                    desc = re.search(r'^\((.+?)\)', descs).group(1)

                if len(sizev) == 1:
                    if not is_number(sizev[0]):
                        Util.print_warning(f"img size '{sizev[0]}' invalid, default to 50%")
                        sizev[0] = "50"
                    section.append(f"<p></p><img src=\"{args['pic_path']}/{linkv[0]}\" style=\"display: block; margin: 0 auto;width: {sizev[0]}%;\" alt=\"err! email me if you need\"><p></p>")
                    if desc:
                        section.append(f"<figure><figcaption>{desc}</figcaption></figure>")
                else:
                    section.append("<p></p>")
                    margin_left = (100 - sum(int(size) for size in sizev)) // (len(sizev) + 1)
                    for i, size in enumerate(sizev):
                        if not is_number(size):
                            Util.print_error(f"Invalid image size '{sizev[i]}', default to 30%")
                            size = "30"
                        section.append(f"<img src=\"{args['pic_path']}/{linkv[i]}\" style=\"width: {size}%; margin-left: {margin_left}%;\" alt=\"err! email me if you need\">")
                    section.append("<p></p>")
                    if desc:
                        section.append(f"<figure><figcaption>{desc}</figcaption></figure>")
            elif list_item_regex.search(line):
                indent = match.group(1)
                list_item = match.group(2)
                current_indent_level = len(indent)

                if current_indent_level > last_indent_level:
                    indent_count[current_indent_level] += 1
                    section.append("<ul>")
                    in_list = True
                elif current_indent_level < last_indent_level:
                    for i in range(current_indent_level + 1, 100):
                        while indent_count[i] != 0:
                            section.append("</ul>")
                            indent_count[i] -= 1

                list_item = re.sub(r"\$(.*?)\$", r"\(\1\)", list_item)
                list_item = re.sub(r"`(.*?)`", r"<code>\1</code>", list_item)
                section.append(f'<li class="blog_list">{list_item}</li>')
                last_indent_level = current_indent_level

            else:
                if line:
                    processed_line = line
                    processed_line = re.sub(r"\$\$(.*?)\$\$", r"<div>\[ \1 \]</div>", processed_line)
                    processed_line = re.sub(r"\$(.*?)\$", r"\(\1\)", processed_line)
                    processed_line = re.sub(r"`(.*?)`", r"<code>\1</code>", processed_line)
                    section.append(f"<p>{processed_line}</p>")

        if in_list:
            for i in range(100):
                while indent_count[i] != 0:
                    section.append("</ul>")
                    indent_count[i] -= 1

        if in_section:
            section.append("</section>")
            html.append("\n".join(section))

        toc = []
        if h1v:
            toc.append("<ul>")
            for h1 in h1v:
                toc.append(f"<li><a class=\"toch1\" href=\"#{h1.name_toc}\">{h1.name_real}</a>")
                if h1.h2v:
                    toc.append("<ul>")
                    for h2 in h1.h2v:
                        toc.append(f"<li><a class=\"toch2\" href=\"#{h2.name_toc}\">{h2.name_real}</a>")
                        if h2.h3v:
                            toc.append("<ul>")
                            for h3 in h2.h3v:
                                toc.append(f"<li><a class=\"toch3\" href=\"#{h3.name_toc}\">{h3.name_real}</a></li>")
                            toc.append("</ul>")
                        toc.append("</li>")
                    toc.append("</ul>")
                toc.append("</li>")
            toc.append("</ul>")
        
        tocjsmap2 = ["const toch2map = {"]
        tocjsmap3 = ["const toch3map = {"]

        if h1v:
            for h1 in h1v:
                for h2 in h1.h2v:
                    tocjsmap2.append(f"'{h2.name_toc}' :{{ h1: '{h1.name_toc}' }},")
                    for h3 in h2.h3v:
                        tocjsmap3.append(f"'{h3.name_toc}' :{{ h1: '{h1.name_toc}', h2: '{h2.name_toc}' }},")
        tocjsmap2.append("}")
        tocjsmap3.append("}")
        return "\n".join(toc), "\n".join(tocjsmap2+tocjsmap3), "\n".join(html)




