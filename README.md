# minimal-page

[demo](https://wenqingqian3.github.io)
```txt
├── README.md
├── _kernel
│   ├── html-template
│   │   ├── blog.html                :: Blog page template
│   │   ├── blog_index.html          :: Blog index page template
│   │   ├── blog_index_with_toc.html :: Blog index page with table of contents
│   │   ├── download.html            :: Download page template
│   │   ├── index.html               :: Homepage template
│   │   └── search_metadata.txt      :: Do not modify
│   └── *.py                         :: Generator source files
├── index.html                       :: Entry point for GitHub Pages
├── only_mod_here.toml               :: Website configuration file
├── render                           :: Directory for CSS and JS files
├── run.py                           :: Entry point for the generator
├── user
│   ├── blog
│   │   └── cates
│   │       ├── pic                  :: Directory for images
│   │       └── *.html               :: HTML files under categories
│   ├── _blog_history                :: Previous generation files are moved here
│   └── blog_online
│       ├── _autogen_row_online_metadata.txt :: Row layout for online metadata
│       ├── note
│       │   ├── *.md                 :: Note files
│       │   └── pic                  :: Images related to notes
│       └── online_metadata.yml      :: Online metadata file
└── webroot
    ├── assets
    │   ├── download
    │   │   └── type
    │   │       └── *                :: Download files organized by type
    │   ├── download.html            :: Download page
    │   ├── other.html               :: Other pages
    │   ├── redirect-page
    │   │   └── *                    :: Redirect pages
    │   └── resume.pdf               :: Resume file
    ├── blog
    │   ├── _                        :: Stores notes for reprinted content
    │   │   └── *.html               :: HTML files for reprinted notes
    │   └── cates
    │       └── *.html               :: Blog pages under categories
    ├── blog.html                    :: Blog index page
    └── index.html                   :: Homepage
```
### Supported Markdown-to-HTML syntax
1. #, ##, ### Three levels of headings
2. `-` List
3. `![size1,size2...](link1,link2...)(description(Optional))` Multiple images in one line, where `size` represents the percentage of the image’s display width in a line
4. `$eq$` Inline formula, `$$eq$$` Block formula (support multi-line), \`code\` Inline code
5. Support link `[name](link)`, link must match http(s)://*
6. Support reference `> content`

### Features
1. Multi-category support: `category: cate1 cate2` 
   You can specify multiple categories for a post, but the source file must be placed in a specific category directory, which also contains the images. The directory name will be used as the primary category name, and a page will be generated only in this category.
   Sub-categories will be used to generate links in the blog index page.
2. Reprint support: You can reprint articles, and include your own notes alongside them. 
3. Support search `command + K`, search engine will calculate the relevance scores for all blogs, and you can easily adjust the threshold to en/disable some of them.
   - Scale the content score based on the file size.
   - Use 'name' to enforce that the target content must include the specified name.

### usage
```shell
# minimal-page/
python run.py
```
### TODO & Notice

```txt
[  %]blog_history is not support now
[%%%]auto clean generated file 
[  %]rewrite the format modified markdown to source
[ %%]support ordered list (hard)

```