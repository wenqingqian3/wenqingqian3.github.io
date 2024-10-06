#pragma once
#include <fstream>
#include <iostream>
#include <sstream>
#include "blog_html.h"
#include <string>
#include <vector>
#include <map>
#include <any>
#include "config.h"
using namespace std;

struct blog {
	string title;
	string author;
	string date;
	int date_year, date_month, date_day;
	string description;
	string type;
	string language;
	string category;
	vector<string> categories;
	string pri_category;
	string target_file_name;
	string ps; 
	string content;
	string redirect;
	// render

	// blog index html
	// category
	//     - title (data, type, ps)
	//       description

	// blog html
	// title
	// date, author
	// description

	void generate(){
		//* gen time 
		std::stringstream ss(date);
		std::string token;
		std::getline(ss, token, '-');
		date_year = std::stoi(token);
		std::getline(ss, token, '-');
		date_month = std::stoi(token);
		std::getline(ss, token, '-');
		date_day = std::stoi(token);
		//* gen cate
		std::stringstream space_split(category);
		std::string cate;
		while( space_split >> cate ){
			categories.emplace_back(cate);
		}

		// 这里是生成blog对应的html文件, 如果是pdf只用在generator中对blog.html设置链接就行
		if(redirect == "" || redirect == "none"){
			string filename = blog_html_source_path + pri_category + "/" + target_file_name + ".html";

			ofstream outfile(filename);
			if (!outfile) {
				cerr << "无法打开文件: " << filename << endl;
				return;
			}
			if ( language == "english" )
				outfile << blog_html_english_head;
			else
				outfile << blog_html_chinese_head;

			auto vs = blog_markdown2html();

			outfile << "<div class=\"container\"><aside class=\"toc-container\"><nav class=\"toc-sidebar\">";

			outfile << vs[1];

			outfile << "</nav></aside><main>";

			// header
			outfile << "<div class='disp-toc-header'>\n<h1>" + title + "</h1><h2 style=\"font-family: 'ZCOOL XiaoWei', regular;\">" + author + ' ' + date;
			if(ps!=""&&ps!="none") outfile << " " << ps << "</h2>" << endl;
			else outfile << "</h2>" << endl;

			if(description!=""&&description!="none") outfile << "<p>" + description + "</p>";
			outfile << "</div>";

			outfile << vs[0];

			outfile << blog_html_tail_1;

			outfile << "<script>" << vs[2] << "\n</script>";

			outfile << blog_html_tail_2;
			outfile.close();
		}
	}

	std::vector<std::string> blog_markdown2html(){
		std::ifstream inputFile("../user/blog/" + pri_category + "/" + target_file_name + ".md");
		std::stringstream buffer;
		buffer << inputFile.rdbuf();
		std::string markdown = buffer.str();
		extern std::vector<std::string> markdown_to_html(
			const std::string& markdown, std::map<std::string, std::any>);
		auto html = markdown_to_html(markdown, {{"pic_path", blog_pic_source_path + pri_category}});

		return html;
	}
};