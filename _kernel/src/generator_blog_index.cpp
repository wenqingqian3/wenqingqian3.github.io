#include "blog.h"
#include "config.h"
#include "util.h"
#include <set>
#include <filesystem>
#include <sstream>

// namespace fs = std::filesystem;

// // 获取指定目录下的所有子文件夹
// std::vector<fs::path> listDirectories(const std::string& path) {
// 	std::vector<fs::path> directories;
// 	for (const auto& entry : fs::directory_iterator(path)) {
// 		if (entry.is_directory()) {
// 			directories.push_back(entry.path());
// 		}
// 	}
// 	return directories;
// }

// // 获取指定目录下的所有 .cpp 文件，并去掉后缀
// std::vector<std::string> listCppFiles(const fs::path& directory) {
// 	std::vector<std::string> cppFiles;
// 	for (const auto& entry : fs::directory_iterator(directory)) {
// 		if (entry.is_regular_file() && entry.path().extension() == ".cpp") {
// 			cppFiles.push_back(entry.path().stem().string()); // 去掉 .cpp 后缀
// 		}
// 	}
// 	return cppFiles;
// }

// 生成blog.html 索引页面
void generate_blog_index(vector<blog>& blogvec, bool if_gen_blog_index_toc){
	set<string> categories;

	for(auto& blog : blogvec){
		blog.generate();
		for( auto& cate: blog.categories)
			categories.emplace(cate);
	}

	// 时间倒序
	// std::reverse(blogvec.begin(), blogvec.end());
	sort(blogvec.begin(), blogvec.end(), [&](auto& bvl, auto& bvr){
		if( bvl.date_year != bvr.date_year ) return bvl.date_year > bvr.date_year;
		else if( bvl.date_month != bvr.date_month ) return bvl.date_month > bvr.date_month;
		else if( bvl.date_day != bvr.date_day ) return bvl.date_day > bvr.date_day;
		return true;
	});

	extern std::vector<std::string> markdown_to_html(
		const std::string& markdown, std::map<std::string, std::any>);
	ofstream outfile(blog_index_path);
	if( !if_gen_blog_index_toc ){
		outfile << blog_index_head;
		
		for(auto& cate : categories){
			outfile << "<section><h1>" + convert_udl_to_space(cate) + "</h1><ul>\n";
			for(auto& blog : blogvec){
				for(auto& mcate : blog.categories){
					if(mcate == cate){
						bool isredirect = !(blog.redirect == "" || blog.redirect == "none");
						bool isonline = (blog.type == "online");
						string href_class = isredirect ? 
											(isonline ? "class=\"online\"" : "class=\"assets\"") 
											: "class=\"html\"";
						string path = isredirect ? 
									( isonline ? blog.redirect : "./assets/redirect-page/" + blog.redirect) 
									: blog_html_source_path + blog.pri_category + "/" + blog.target_file_name + ".html";

						outfile << "<li><a " << href_class << " href=\""+path+"\">"+blog.title+"</a> ( "+blog.date+", "+blog.type;
						if(blog.ps != "" && blog.ps != "none"){
							outfile << ", "+blog.ps;
						}
						outfile << " )";
						if(blog.description != "" && blog.description != "none"){
							outfile << "<p style=\"color:#adafb1;\">"+blog.description+"</p>";
						}
						outfile << "</li>\n";
					}
				}
			}
			outfile << "</ul></section>\n";
		}

		outfile << blog_index_tail;
	}else{

		// build index markdown then markdown-to-html to get html, toc, tocmap
		std::stringstream index_md;
		for(auto& cate : categories){
			index_md << "# " << convert_udl_to_space(cate) << '\n';
			for(auto& blog : blogvec){
				for(auto& mcate : blog.categories){
					if(mcate == cate){
						bool isredirect = !(blog.redirect == "" || blog.redirect == "none");
						bool isonline = (blog.type == "online");
						string href_class = isredirect ? 
											(isonline ? "class=\"online\"" : "class=\"assets\"") 
											: "class=\"html\"";
						string path = isredirect ? 
									( isonline ? blog.redirect : "./assets/redirect-page/" + blog.redirect) 
									: blog_html_source_path + blog.pri_category + "/" + blog.target_file_name + ".html";

						index_md << "- <a " << href_class << " href=\"" << path << "\">" << blog.title << "</a> ( " << blog.date << ", " << blog.type;
						if(blog.ps != "" && blog.ps != "none"){
							index_md << ", " << blog.ps;
						}
						index_md << " )\n";
						if(blog.description != "" && blog.description != "none"){
							
							index_md << "  !@#$" << ltrim(blog.description) << '\n';
						}
					}
				}
			}
		}

		auto vs = markdown_to_html(index_md.str(), {});

		outfile << blog_index_toc_head_1;

		outfile << "<div class=\"container\"><aside class=\"toc-container\"><nav class=\"toc-sidebar\">";

		outfile << vs[1];

		outfile << "</nav></aside>";

		outfile << blog_index_toc_head_2;

		outfile << vs[0];

		outfile << blog_index_toc_tail_1;

		outfile << "<script>" << vs[2] << "\n</script>";

		outfile << blog_index_toc_tail_2;
		outfile.close();
	}
}