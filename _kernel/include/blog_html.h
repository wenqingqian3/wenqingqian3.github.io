#pragma once
#include <string>
using namespace std;
inline string blog_html_english_head = R"xxxxx(

<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Blog</title>
	<link rel="icon" href="../../../render/icon/appletree.png" type="image/png">
	<link href="../../../render/fonts.css" rel="stylesheet">
	<link href="../../../render/style_base.css" rel="stylesheet">
	<link href="../../../render/blog.css" rel="stylesheet">
	<link href="../../../render/style_english.css" rel="stylesheet">
	<link rel="preconnect" href="https://fonts.googleapis.com">
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
	<link href="https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=ZCOOL+XiaoWei&display=swap" rel="stylesheet">
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
	<link href="../../../render/sidebar.css" rel="stylesheet">
	<link href="../../../render/common.css" rel="stylesheet">
	<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
<main>
)xxxxx";

inline string blog_html_tail = R"xxxxx(
	
	<div class="settings-menu">
		<button class="settings-button">Control</button>
		<div class="settings-options">
			<a class="settings-button" href="../../index.html">home</a>
			<a style="color: var(--basic-black);">width <button id="adjustWidth-add" class="settings-inner-button">+</button> / <button id="adjustWidth-sub" class="settings-inner-button">-</button></a>
			<a class="settings-button" href="../../_blog.html">back to blog</a>
		</div>
	</div>
</main>


<script src="../../../render/sidebar.js"></script> 
<script src="../../../render/common.js"></script> 

</body>
</html>

)xxxxx";

inline string blog_html_chinese_head = R"xxxxx(

<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Blog</title>
	<link rel="icon" href="../../../render/icon/appletree.png" type="image/png">
	<link href="../../../render/fonts.css" rel="stylesheet">
	<link href="../../../render/blog.css" rel="stylesheet">
	<link href="../../../render/style_base.css" rel="stylesheet">
	<link href="../../../render/style_chinese.css" rel="stylesheet">
	<link rel="preconnect" href="https://fonts.googleapis.com">
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
	<link href="https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=ZCOOL+XiaoWei&display=swap" rel="stylesheet">
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
	<link href="../../../render/sidebar.css" rel="stylesheet">
	<link href="../../../render/common.css" rel="stylesheet">
	<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
<main>
)xxxxx";

inline string blog_index_head = R"xxxxx(

<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Blog</title>
	<link rel="icon" href="../render/icon/appletree.png" type="image/png">
	<link href="../render/fonts.css" rel="stylesheet">
	<link href="../render/style_base.css" rel="stylesheet">
	<link href="../render/style_english.css" rel="stylesheet">
	<link rel="preconnect" href="https://fonts.googleapis.com">
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
	<link href="https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=ZCOOL+XiaoWei&display=swap" rel="stylesheet">
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
	<link href="../render/sidebar.css" rel="stylesheet">
	<link href="../render/common.css" rel="stylesheet">
</head>
<body>
<main>
	<header>Notes</header>
	<div class='disp-toc-header'><p>This page and the following HTML-type web pages are all built by the automatic generator in this repository. The corresponding markdown source files of these HTML-type web pages can be found in the repository</p></div>
)xxxxx";

inline string blog_index_tail = R"xxxxx(
		<div class="settings-menu">
		<button class="settings-button">Control</button>
		<div class="settings-options">
			<a class="settings-button" href="./index.html">home</a>
			<a style="color: var(--basic-black);">width <button id="adjustWidth-add" class="settings-inner-button">+</button> / <button id="adjustWidth-sub" class="settings-inner-button">-</button></a>
		</div>
	</div>
</main>


<script src="../render/sidebar.js"></script> 
<script src="../render/common.js"></script> 

</body>
</html>

)xxxxx";