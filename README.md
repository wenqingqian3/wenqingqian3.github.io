# minimal-page

[demo](https://wenqingqian3.github.io)

```txt
|- _kernel : Generator source file, partially auto-generated
|- render : Web page render, including css, js, icon, etc.
|- user \- blog : Markdown source files must be split into several categories
                  and the category written in the markdown must match the directory name
        |- _blog_history : Auto-generated files in webroot/_blog/*
        |- blog_online : Reprint and note
|- webroot \- index.html (homepage) manually created
           |- blog.html auto-generated
           |- assets :     \- resume.pdf
           (resource repo) |- download.html -> ./download/
                           |- redirect-page : Blog redirect pages should be placed here
```

### Supported Markdown-to-HTML syntax
1. #, ##, ### Three levels of headings
2. `-` List
3. `![size1,size2...](link1,link2...)(description(Optional))` Multiple images in one line, where `size` represents the percentage of the image’s display width in a line
4. `$eq$` Inline formula, `$$eq$$` Block formula, \`code\` Inline code

### Features
1. Multi-category support: `category: cate1 cate2`
   You can specify multiple categories for a post, but the source file must be placed in a specific category directory, which also contains the images. The directory name will be used as the primary category name, and a page will be generated only in this category.
   Sub-categories will be used to generate links in the blog index page.
2. Reprint support: You can reprint articles, and include your own notes alongside them. 

### usage
```shell
cd _kernel
python run.py -c all
```
