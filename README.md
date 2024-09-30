# minimal-page

[demo](https://github.com/wenqingqian3/wenqingqian3.github.io)

```txt
文件结构
|- _kernel : 生成器源文件, 部分代码自动生成
|- render : 页面渲染文件
|- user \- blog : 必须设置category, 里面存放markdown, 文件内部cate要与文件夹名对应
        |- _blog_history : 自动生成, 上一版本的 webroot/_blog/*
|- webroot 网站根目录 \- index.html (主页) 手动修改
                     |- _blog.html 自动生成
                     |- assets : 存放资源 \- resume.pdf
                                         |- download.html -> ./download/
                                         |- redirect-page : redirect blog 存放在这(相对路径) 
                                             可以在kernel/src/generator_blog.cpp 50行改

markdown转html支持格式
1. #, ##, ### 三级标题
2. - 支持嵌套无序列表
3. ![size1,size2...](link1,link2...)(description(可选)) 单行多图, size为单行宽度百分比
4. $eq$ 行内公式, $$eq$$ 单行公式, `code` 行内代码

cd _kernel
./run.sh
```
