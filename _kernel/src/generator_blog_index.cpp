#include "blog.h"
#include "config.h"
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
		int yearl, yearr, monthl, monthr, dayl, dayr;
		{
			std::stringstream ss(bvl.date);
			std::string token;
			std::getline(ss, token, '-');
			yearl = std::stoi(token);
			std::getline(ss, token, '-');
			monthl = std::stoi(token);
			std::getline(ss, token, '-');
			dayl = std::stoi(token);
		}
		{
			std::stringstream ss(bvr.date);
			std::string token;
			std::getline(ss, token, '-');
			yearr = std::stoi(token);
			std::getline(ss, token, '-');
			monthr = std::stoi(token);
			std::getline(ss, token, '-');
			dayr = std::stoi(token);
		}

		if( yearl != yearr ) return yearl > yearr;
		else if( monthl != monthr ) return monthl > monthr;
		else if( dayl != dayr ) return dayl > dayr;
		return true;

	});

	ofstream outfile(blog_index_path);
	if( !if_gen_blog_index_toc ){
		outfile << blog_index_head;
		
		for(auto& cate : categories){
			outfile << "<section><h1>" + cate + "</h1><ul>\n";
			for(auto& blog : blogvec){
				for(auto& mcate : blog.categories){
					if(mcate == cate){
						bool isredirect = !(blog.redirect == "" || blog.redirect == "none");
						string path = isredirect ? "./assets/redirect-page/" + blog.redirect : blog_html_source_path + blog.pri_category + "/" + blog.target_file_name + ".html";

						outfile << "<li><a href=\""+path+"\">"+blog.title+"</a> ( "+blog.date+", "+blog.type;
						if(blog.ps != "" && blog.ps != "none"){
							outfile << ", "+blog.ps;
						}
						outfile << " )";
						if(blog.description != "" && blog.description != "none"){
							outfile << "<p>"+blog.description+"</p>";
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
			index_md << "# " << cate << '\n';
			for(auto& blog : blogvec){
				for(auto& mcate : blog.categories){
					if(mcate == cate){
						bool isredirect = !(blog.redirect == "" || blog.redirect == "none");
						string path = isredirect ? "./assets/redirect-page/" + blog.redirect : blog_html_source_path + blog.pri_category + "/" + blog.target_file_name + ".html";

						index_md << "- <a href=\"" << path << "\">" << blog.title << "</a> ( " << blog.date << ", " << blog.type;
						if(blog.ps != "" && blog.ps != "none"){
							index_md << ", " << blog.ps;
						}
						index_md << " )\n";
						if(blog.description != "" && blog.description != "none"){
							extern std::string ltrim(const std::string&);
							index_md << "  " << ltrim(blog.description) << '\n';
						}
					}
				}
			}
		}

		extern std::vector<std::string> markdown_to_html(
			const std::string& markdown, std::map<std::string, std::any>);
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