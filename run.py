from _kernel.main import main
from _kernel.util import Util

if __name__ == "__main__":
    main("only_mod_here.toml")


# from colorama import init, Fore
# import re, os
# import traceback
# import numpy as np

# init(autoreset=True)

# class H3:
#     def __init__(self, name_toc, name_real):
#         self.name_toc = name_toc
#         self.name_real = name_real

# class H2:
#     def __init__(self, name_toc, name_real):
#         self.name_toc = name_toc
#         self.name_real = name_real
#         self.h3v = []

# class H1:
#     def __init__(self, name_toc, name_real):
#         self.name_toc = name_toc
#         self.name_real = name_real
#         self.h2v = []

# def unique_toc_name(name, toc_name_set):
#     while name in toc_name_set:
#         name += "_O_o"
#     toc_name_set.add(name)
#     return name

# def is_number(s):
#     return s.isdigit()

# class Util:
#     DEBUG = False
#     @staticmethod
#     def print_warning(message):
#         print(Fore.YELLOW + "[WARNING] " + message)
#     @staticmethod
#     def print_error(message, level = 0):
#         tb = traceback.extract_stack()[-level-1]
#         print(Fore.RED + "[ERROR] " + message + f" :: {tb.filename}, {tb.lineno}")
#     @staticmethod
#     def print_info(message):
#         print(Fore.GREEN + "[INFO] " + message)
#     @staticmethod
#     def print_debug(message):
#         if Util.DEBUG : print(Fore.BLUE + "[DEBUG] " + f'{message}')
#     @staticmethod
#     def replace_invalid_chars(s):
#         return re.sub(r'[^\w]', 'UNVAILD_TOKEN', s)
#     @staticmethod
#     def calculate_relative_path(file_path, target_dir):
#         if Util.is_none(file_path) or Util.is_none(target_dir):
#             raise RuntimeError(f'file-path:{file_path}, target-path:{target_dir}')
#         file_dir = os.path.dirname(file_path)
#         relative_path = os.path.relpath(target_dir, file_dir)
#         return relative_path
#     @staticmethod
#     def convert_udl_to_space(strs):
#         return strs.replace('_', ' ')
#     @staticmethod
#     def is_none(a):
#         return a == "none" or a is None or a.strip() == ""
#     @staticmethod
#     def replace_chinese_punctuation(text):
#         text = text.replace('，', ', ').replace('。', '. ').replace('：', ': ')
#         return text
#     @staticmethod
#     def markdown_to_html(markdown, args):
#         markdown = Util.replace_chinese_punctuation(markdown)

#         toc_name = set()
#         h1v = []
#         html = []
#         section = []
#         in_section = False
#         in_math_block = False
#         in_list = False
#         in_metadata = False
#         skip_metadata = False
#         in_blockquote = False
#         in_codeblock  = False
#         math_block = []
#         list_item_regex = re.compile(r"^(\s*)-\s+(.*)")
#         indent_regex = re.compile(r"^(\s*)(.*)")
#         last_indent_level = -1
#         indent_count = [0] * 100

#         _general_pattern = {
#             "code": [r"`(.*?)`", r"<code>\1</code>"],
#             "block_formula": [r"^\s?\$\$(.*?)\$\$\s?$", r"<div>\[ \1 \]</div>"],
#             "inline_formula": [r"\$(.*?)\$", r"\(\1\)"],
#             "link" : [r"\[(.*?)\]\((.*?)\)", r'<a class="online" href="\2">\1</a>'],
#         }

#         def general_sub(item, **kargs):
#             for key in kargs:
#                 if key not in _general_pattern:
#                     Util.print_error(f"invaild name {key} for disable the genernal_pattern", 1)
#             for key, (pattern, replacement) in _general_pattern.items():
#                 if kargs.get(key) is False:
#                     continue
#                 item = re.sub(pattern, replacement, item)
            
#             return item

#         lines = markdown.split('\n')

#         for line in lines:
#             if re.match(r"^\s*```.*$", line):
#                 if in_codeblock:
#                     section.append("</code></pre>")
#                     in_codeblock = False
#                 else:
#                     if in_blockquote:
#                         section.append("</blockquote>")
#                         in_blockquote = False
#                     language = re.search(r"^\s*```(.*)$", line).group(1).strip()
#                     section.append(f'<pre><code class="language-{language}">')
#                     in_codeblock = True
#                 continue
#             elif in_codeblock:
#                 if in_list and last_indent_level >=0:
#                     num_space = (last_indent_level + 2)
#                     if line.startswith(" " * num_space):
#                         line = line[num_space:]
#                 section.append(line)
#                 continue

#             emptyline = re.sub(r"^\s+|\s+$", "", line)
#             if not emptyline:
#                 if in_blockquote:
#                     section.append("</blockquote>")
#                     in_blockquote = False
#                 continue

#             if emptyline == "---":
#                 if not in_metadata:
#                     in_metadata = True
#                     skip_metadata = True
#                     continue
#                 else:
#                     skip_metadata = False
#                     continue

#             if skip_metadata:
#                 continue

#             line = line.rstrip()



#             match = list_item_regex.search(line)

#             if line and in_list and not list_item_regex.search(line):
#                 match = indent_regex.search(line)
#                 indent = match[1]

#                 if len(indent) == last_indent_level + 2:
#                     item = match[2]
#                     item = general_sub(item)
#                     if item.startswith("!@#$"):
#                         section.append(f"<p style=\"margin-bottom: 0em;color:#adafb1\">{item[4:]}</p>")
#                     else:
#                         if item.startswith(">"):
#                             if len(item) > 2:
#                                 if in_blockquote:
#                                     quote = item[2:].strip()
#                                     if quote != "":
#                                         section.append(f" {quote}")
#                                     else:
#                                         section.append("<p></p>")
#                                 else:
#                                     section.append(f"<blockquote>{item[2:]}")
#                                     in_blockquote = True
#                             else:
#                                 if in_blockquote:
#                                     section.append("<p></p>")
#                             continue
#                         else:
#                             if in_blockquote:
#                                 section.append("</blockquote>")
#                                 in_blockquote = False
#                             section.append(f"<p style=\"margin-bottom: 0em;\">{item}</p>")
#                     continue
#                 else:
#                     if in_blockquote:
#                         section.append("</blockquote>")
#                         in_blockquote = False
#                     for i in range(100):
#                         while indent_count[i] != 0:
#                             section.append("</ul>")
#                             indent_count[i] -= 1
#                     in_list = False
#                     last_indent_level = -1


#             if not re.match(r"^\$\$$", line) and in_math_block:
#                 math_block.append(line)

#             elif re.match(r"^\$\$$", line) and not in_math_block:
#                 in_math_block = True

#             elif re.match(r"^\$\$$", line) and in_math_block:
#                 section.append("<div>\\[" + "\\]\\[".join(math_block) + "\\]</div>")
#                 math_block = []
#                 in_math_block = False

#             elif re.match(r"^# .+", line):
#                 if in_section:
#                     section.append("</section>")
#                     html.append("\n".join(section))
#                     section = []
#                 section.append("<section>")
#                 h1name = unique_toc_name(line[2:], toc_name)
#                 section.append(f"<h1 id=\"{h1name}\">{line[2:]}</h1>")
#                 in_section = True
#                 h1v.append(H1(name_toc=h1name, name_real=line[2:]))

#             elif re.match(r"^## .+", line):
#                 h2name = unique_toc_name(line[3:], toc_name)
#                 section.append(f"<h2 id=\"{h2name}\">{line[3:]}</h2>")
#                 if not h1v:
#                     Util.print_error("must have h1 before h2")
#                 h1v[-1].h2v.append(H2(name_toc=h2name, name_real=line[3:]))

#             elif re.match(r"^### .+", line):
#                 h3name = unique_toc_name(line[4:], toc_name)
#                 section.append(f"<h3 id=\"{h3name}\">{line[4:]}</h3>")
#                 if not h1v:
#                     Util.print_error("must have h1 before h3")
#                 if not h1v[-1].h2v:
#                     Util.print_error("must have h2 before h3")
#                 h1v[-1].h2v[-1].h3v.append(H3(name_toc=h3name, name_real=line[4:]))

#             elif re.match(r"^#### .+", line):
#                 Util.print_warning("currently not support h4, treat as plain text")
#                 section.append(f"<p>{line[5:]}</p>")
#             elif re.match(r"^##### .+", line):
#                 Util.print_warning("currently not support h5, treat as plain text")
#                 section.append(f"<p>{line[6:]}</p>")
#             elif re.match(r"^!\[(.+?)\].*", line):
#                 parts = re.search(r'^!\[(.+?)\]\((.+?)\)(.*)', line)

#                 sizes = parts.group(1)
#                 sizev = [s.strip() for s in sizes.split(',')]

#                 links = parts.group(2)
#                 linkv = [l.strip() for l in links.split(',')]
                
#                 descs = parts.group(3)
#                 desc  = ""
#                 if re.match(r'^\((.+?)\)', descs):
#                     desc = re.search(r'^\((.+?)\)', descs).group(1)

#                 if len(sizev) == 1:
#                     if not is_number(sizev[0]):
#                         Util.print_warning(f"img size '{sizev[0]}' invalid, default to 50%")
#                         sizev[0] = "50"
#                     section.append(f"<p></p><img src=\"{args['pic_path']}/{linkv[0]}\" style=\"display: block; margin: 0 auto;width: {sizev[0]}%;\" alt=\"err! email me if you need\"><p></p>")
#                     if desc:
#                         section.append(f"<figure><figcaption>{desc}</figcaption></figure>")
#                 else:
#                     section.append("<p></p>")
#                     margin_left = (100 - sum(int(size) for size in sizev)) // (len(sizev) + 1)
#                     for i, size in enumerate(sizev):
#                         if not is_number(size):
#                             Util.print_error(f"Invalid image size '{sizev[i]}', default to 30%")
#                             size = "30"
#                         section.append(f"<img src=\"{args['pic_path']}/{linkv[i]}\" style=\"width: {size}%; margin-left: {margin_left}%;\" alt=\"err! email me if you need\">")
#                     section.append("<p></p>")
#                     if desc:
#                         section.append(f"<figure><figcaption>{desc}</figcaption></figure>")
#             elif list_item_regex.search(line):
#                 indent = match.group(1)
#                 list_item = match.group(2)
#                 current_indent_level = len(indent)
                
#                 if in_blockquote:
#                     section.append("</blockquote>")
#                     in_blockquote = False

#                 if current_indent_level > last_indent_level:
#                     indent_count[current_indent_level] += 1
#                     section.append("<ul>")
#                     in_list = True
#                 elif current_indent_level < last_indent_level:
#                     for i in range(current_indent_level + 1, 100):
#                         while indent_count[i] != 0:
#                             section.append("</ul>")
#                             indent_count[i] -= 1

#                 list_item = general_sub(list_item, block_formula=False)
#                 section.append(f'<li class="blog_list">{list_item}</li>')
#                 last_indent_level = current_indent_level

#             else:
#                 if line:
#                     item = line.strip()
#                     if item.startswith(">"):
#                         if len(item) > 2:
#                             if in_blockquote:
#                                 quote = item[2:].strip()
#                                 if quote != "":
#                                     section.append(f" {quote}")
#                                 else:
#                                     section.append("<p></p>")
#                             else:
#                                 section.append(f"<blockquote>{item[2:]}")
#                                 in_blockquote = True
#                         else:
#                             if in_blockquote:
#                                 section.append("<p></p>")
#                         continue
#                     else:
#                         if in_blockquote:
#                             section.append("</blockquote>")
#                             in_blockquote = False
#                     processed_line = line
#                     processed_line = general_sub(processed_line)
#                     section.append(f"<p>{processed_line}</p>")
#                 else:
#                     Util.print_error("empty line")

#         if in_list:
#             if in_blockquote:
#                 section.append("</blockquote>")
#                 in_blockquote = False
#             for i in range(100):
#                 while indent_count[i] != 0:
#                     section.append("</ul>")
#                     indent_count[i] -= 1

#         if in_section:
#             if in_blockquote:
#                 section.append("</blockquote>")
#                 in_blockquote = False
#             section.append("</section>")
#             html.append("\n".join(section))

#         toc = []
#         if h1v:
#             toc.append("<ul>")
#             for h1 in h1v:
#                 toc.append(f"<li><a class=\"toch1\" href=\"#{h1.name_toc}\">{h1.name_real}</a>")
#                 if h1.h2v:
#                     toc.append("<ul>")
#                     for h2 in h1.h2v:
#                         toc.append(f"<li><a class=\"toch2\" href=\"#{h2.name_toc}\">{h2.name_real}</a>")
#                         if h2.h3v:
#                             toc.append("<ul>")
#                             for h3 in h2.h3v:
#                                 toc.append(f"<li><a class=\"toch3\" href=\"#{h3.name_toc}\">{h3.name_real}</a></li>")
#                             toc.append("</ul>")
#                         toc.append("</li>")
#                     toc.append("</ul>")
#                 toc.append("</li>")
#             toc.append("</ul>")
        
#         tocjsmap2 = ["const toch2map = {"]
#         tocjsmap3 = ["const toch3map = {"]

#         if h1v:
#             for h1 in h1v:
#                 for h2 in h1.h2v:
#                     tocjsmap2.append(f"'{h2.name_toc}' :{{ h1: '{h1.name_toc}' }},")
#                     for h3 in h2.h3v:
#                         tocjsmap3.append(f"'{h3.name_toc}' :{{ h1: '{h1.name_toc}', h2: '{h2.name_toc}' }},")
#         tocjsmap2.append("}")
#         tocjsmap3.append("}")
#         return "\n".join(toc), "\n".join(tocjsmap2+tocjsmap3), "\n".join(html)

# class AdaptiveScaler:
#     def __init__(self, target_min=1, target_max=10):
#         self.target_min = target_min
#         self.target_max = target_max
#         self.lower_bound = None
#         self.upper_bound = None
#         self.min_val = None
#         self.max_val = None
#         self.scale_factor = None

#     def fit(self, sequence):
#         """
#         Fit the scaler to the input sequence.
        
#         :param sequence: Input sequence of numbers
#         """
#         if not sequence:
#             raise ValueError("Input sequence cannot be empty")

#         arr = np.array(sequence)

#         # Calculate Q1, Q3 and IQR
#         q1, q3 = np.percentile(arr, [25, 75])
#         iqr = q3 - q1

#         # Define bounds for outliers
#         self.lower_bound = q1 - 1.5 * iqr
#         self.upper_bound = q3 + 1.5 * iqr

#         # Clip the array to remove extreme outliers
#         arr_clipped = np.clip(arr, self.lower_bound, self.upper_bound)

#         # Store min and max values for scaling
#         self.min_val = arr_clipped.min()
#         self.max_val = arr_clipped.max()

#         # Calculate the optimal scale factor
#         raw_range = self.max_val - self.min_val
#         target_range = self.target_max - self.target_min
#         self.scale_factor = min(target_range / raw_range, 1.0)

#     def transform(self, value):
#         """
#         Transform a single value or a sequence of values using the fitted scaler.
        
#         :param value: A single number or a sequence of numbers
#         :return: Scaled value(s) as integer(s)
#         """
#         if self.scale_factor is None:
#             raise ValueError("Scaler must be fitted before transform can be called")

#         # Handle both single value and sequence
#         is_single_value = np.isscalar(value)
#         arr = np.array([value]) if is_single_value else np.array(value)

#         # Clip to bounds
#         arr_clipped = np.clip(arr, self.lower_bound, self.upper_bound)

#         # Scale and shift
#         arr_scaled = (arr_clipped - self.min_val) * self.scale_factor + self.target_min

#         # Round to nearest integer
#         result = np.round(arr_scaled).astype(int)

#         # Ensure the results are within the target range
#         result = np.clip(result, self.target_min, self.target_max)

#         return int(result[0]) if is_single_value else result.tolist()

#     def fit_transform(self, sequence):
#         """
#         Fit the scaler to the input sequence and transform it.
        
#         :param sequence: Input sequence of numbers
#         :return: Scaled sequence as a list of integers
#         """
#         self.fit(sequence)
#         return self.transform(sequence)
    
# markdown = r'''

# - list
#   ```txt
#   sf
#   ```
#   - list
#     ```tdt
#     df
#     ```

# '''

# Util.markdown_to_html(markdown, None)