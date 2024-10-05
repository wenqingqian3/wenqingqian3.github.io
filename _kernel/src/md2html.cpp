#include <iostream>
#include <fstream>
#include <sstream>
#include <regex>
#include <string>
#include <vector>
#include <set>
#include <map>
#include <any>

#include "config.h"
#include "blog.h"
#include "blog_html.h"

struct h2;struct h3;

struct h1 {
	std::string name_toc;
	std::string name_real;
	std::vector<h2> h2v; 
};

struct h2 {
	std::string name_toc;
	std::string name_real;
	std::vector<h3> h3v;
};

struct h3 {
	std::string name_toc;
	std::string name_real;
};



std::string unique_toc_name(std::string name, auto&& sets){
	// for
	while(sets.count(name)){
		name += "_O_o";
	}

	sets.emplace(name);
	return name;
}

bool is_number(std::string str){
	for(auto& c: str){
		if(c > '9' || c < '0') return false;
	}
	return true;
}


//* args: pic_path string required 
std::vector<std::string> markdown_to_html(const std::string& markdown, std::map<std::string, std::any> args) {
	std::set<std::string> toc_name;
	std::vector<h1> h1v;
	std::stringstream html;
	std::stringstream section;
	std::istringstream iss(markdown);
	std::string line;
	bool inSection = false;
	bool inMathBlock = false;
	bool inList = false;
	bool inMetadata = false;
	bool skipMetadata = false;
	std::stringstream mathBlock;
	std::regex listItemRegex(R"(^(\s*)-\s+(.*))");
	std::regex IndentRegex(R"(^(\s*)(.*))");

	int lastIndentLevel = -1;
	int IndentCount[100];
	memset(IndentCount, 0 ,sizeof(IndentCount));

	while (std::getline(iss, line)) {
		std::string emptyline = std::regex_replace(line, std::regex("^\\s+|\\s+$"), "");
		if (emptyline.empty()) continue;

		if (emptyline == "---") {
			if (!inMetadata) {
				inMetadata = true;
				skipMetadata = true;
				continue;
			} else {
				skipMetadata = false;
				continue;
			}
		}

		if (skipMetadata) continue;

		std::smatch match;
		std::regex_search(line, match, listItemRegex);

		if (!line.empty() && inList && !std::regex_search(line, listItemRegex)) {
			std::smatch match;
			std::regex_search(line, match, IndentRegex);
			std::string indent = match[1];

			if(indent.length() == lastIndentLevel + 2){
				std::string item = match[2];

				// 列表中有单行公式
				item = std::regex_replace(item, std::regex("^\\s?\\$\\$(.*?)\\$\\$\\s?$"), "<div>\\[ $1 \\]</div>");
				
				item = std::regex_replace(item, std::regex("\\$(.*?)\\$"), "\\($1\\)");
				item = std::regex_replace(item, std::regex("\\`(.*?)\\`"), "<code>$1</code>");
				section << "<p style=\"margin-bottom: 0em;\">" << item << "</p>" << std::endl;
				continue;
			}else{
				for(int i = 0; i < 100; i ++){
					while(IndentCount[i] != 0){
						section << "</ul>" << std::endl;
						IndentCount[i] --;
					}
				}
				inList = false;
				lastIndentLevel = -1;
			}
		}

		// Process headers
		if (!std::regex_match(line, std::regex("^\\$\\$")) && inMathBlock) {
			mathBlock << line << std::endl;
		} else if (std::regex_match(line, std::regex("^# .+"))) {
			if (inSection) {
				section << "</section>" << std::endl;
				html << section.str();
				section.str("");
				section.clear();
			}
			section << "<section>" << std::endl;
			auto h1name = unique_toc_name(line.substr(2), toc_name);
			section << "<h1 id=\"" << h1name << "\">" << line.substr(2) << "</h1>" << std::endl;
			inSection = true;

			h1v.emplace_back(h1{.name_toc=h1name, .name_real=line.substr(2)});

		} else if (std::regex_match(line, std::regex("^## .+"))) {
			auto h2name = unique_toc_name(line.substr(3), toc_name);
			section << "<h2 id=\"" << h2name << "\">" << line.substr(3) << "</h2>" << std::endl;

			if(h1v.empty()){
				std::cout << "[ERROR] must have h1 before h2\n";
				exit(0);
			}
			h1v.back().h2v.emplace_back(h2{.name_toc=h2name, .name_real=line.substr(3)});

		} else if (std::regex_match(line, std::regex("^### .+"))) {
			auto h3name = unique_toc_name(line.substr(4), toc_name);
			section << "<h3 id=\"" << h3name << "\">" << line.substr(4) << "</h3>" << std::endl;

			if(h1v.empty()){
				std::cout << "[ERROR] must have h1 before h3\n";
				exit(0);
			}			
			if(h1v.back().h2v.empty()){
				std::cout << "[ERROR] must have h2 before h3\n";
				exit(0);
			}
			h1v.back().h2v.back().h3v.emplace_back(h3{.name_toc=h3name, .name_real=line.substr(4)});

		} else if (std::regex_match(line, std::regex("^#### .+"))) {
			// not support currently, treat as ###
			std::cout << "[ERROR] not support h4 #### currently, treat as text and toc will not contain it\n";
			section << "<p>" << line.substr(5) << "</p>" << std::endl;
		// Process images
		} else if (std::regex_match(line, std::regex("^!\\[(.+?)\\].*"))) {
			std::string img_line = line;
			std::smatch match;
			std::regex_search(line, match, std::regex("^!\\[(.+?)\\].*"));
			std::string sizes = match[1];

			std::vector<std::string> sizev;
			std::string size_tmp;
			for(auto c : sizes){
				if( c == ' ' ) continue;
				if( c == ',' ) {
					sizev.emplace_back(size_tmp);
					size_tmp = "";
				}else{
					size_tmp += c;
				}
			}
			if (size_tmp != "") sizev.emplace_back(size_tmp);


			std::vector<std::string> linkv;
			std::string link_tmp;
			std::string desc;

			int ptype = 0;
			int turn = 1;
			int ppcnt = 0;
			for(auto c : img_line){
				if( ptype == 0 && c == ']' ){
					ptype = 1;
					continue;
				}
				if( ptype == 0 ) continue;
				if( turn != 2 && c == ' ' ) continue;

				if( turn == 1 ){
					if( c == '(' ) {
						ppcnt ++;
						if(ppcnt == 1) continue;
					}else if( c == ')' ){
						ppcnt --;
					}

					if( ppcnt == 0 ){
						turn = 2;
						if( link_tmp != "" ) linkv.emplace_back(link_tmp);
					}

					if( c == ',' ) {
						linkv.emplace_back(link_tmp);
						link_tmp = "";
					}else{
						link_tmp += c;
					}

				}else{
					if( c == '(' ) {
						ppcnt ++;
						if(ppcnt == 1) continue;
					}else if( c == ')' ){
						ppcnt --;
						if(ppcnt == 0) continue;
					}
					
					desc += c;
				}
			}
			
			if(sizev.size() == 1){
				if(!is_number(sizev[0])){
					std::cout << "[WARNING] img format : ![size...](path...)(optional: description), need size... but "
							  << sizev[0] << ", use 50\% as default"<< std::endl;
					sizev[0] = "50";
				}

				section << "<p></p><img src=\"" << std::any_cast<std::string>(args["pic_path"]) << "/" << linkv[0]<< "\" style=\"display: block; margin: 0 auto;width: " << sizev[0] << "%;\" alt=\"err! email me if you need\"><p></p>" << std::endl;
				if(!desc.empty()) section << "<figure><figcaption>" << desc << "</figcaption></figure>";
			}else{
				section << "<p></p>";
				int margin_left = (100 - [sizev](){int i=0;for(auto&n:sizev){i+=std::stoi(n);}return i+1;}()) / (sizev.size()+1);
				for (int i = 0; i < sizev.size(); i ++) {
					if(!is_number(sizev[i])){
						std::cout << "[ERROR] img format : ![size...](path...)(optional: description), need size... but "
								  << sizev[0] << std::endl;
						sizev[0] = "30";
					}

					section << "<img src=\"" << std::any_cast<std::string>(args["pic_path"]) << "/" << linkv[i]<< "\" style=\"width: " << sizev[i] << "%; margin-left: " << margin_left << "%;\" alt=\"err! email me if you need\">" << std::endl;
				}
				section << "<p></p>";
				if(!desc.empty()) section << "<figure><figcaption>" << desc << "</figcaption></figure>";
			}
		}
		// Process block math
		else if (std::regex_match(line, std::regex("^\\$\\$")) && !inMathBlock) {
			inMathBlock = true;
			// if (std::regex_match(line, std::regex("^\\$\\$\\$\\$$")))
		} else if (std::regex_match(line, std::regex("^\\$\\$")) && inMathBlock) {
			section << "<div>" << std::endl << "\\[" << std::endl;
			section << mathBlock.str();
			section << "\\]" << std::endl << "</div>" << std::endl;
			mathBlock.str("");
			mathBlock.clear();
			inMathBlock = false;
		}
		// Process list block
		else if (std::regex_search(line, match, listItemRegex)) {
			std::string indent = match[1];
			std::string listItem = match[2];
			int currentIndentLevel = indent.length();

			if (currentIndentLevel > lastIndentLevel) {
				IndentCount[currentIndentLevel] ++;
				section << "<ul>" << std::endl;
				inList = true;
			} else if (currentIndentLevel < lastIndentLevel) {
				for(int i = currentIndentLevel + 1; i < 100; i ++){
					while(IndentCount[i] != 0){
						section << "</ul>" << std::endl;
						IndentCount[i] --;
					}
				}
			}

			listItem = std::regex_replace(listItem, std::regex("\\$(.*?)\\$"), "\\($1\\)");
			listItem = std::regex_replace(listItem, std::regex("\\`(.*?)\\`"), "<code>$1</code>");
			section << "<li>" << listItem << "</li>" << std::endl;
			lastIndentLevel = currentIndentLevel;
		}
		// Process inline math and paragraphs
		else {
			if (!line.empty()) {
				std::string processedLine = line;
				// Replace block math in a single line
				if(std::regex_match(line, std::regex("\\$\\$(.*?)\\$\\$"))){
					processedLine = std::regex_replace(processedLine, std::regex("\\$\\$(.*?)\\$\\$"), "<div>\\[ $1 \\]</div>");
					section << processedLine << std::endl;
				}else{

					// Replace inline math
					processedLine = std::regex_replace(processedLine, std::regex("\\$(.*?)\\$"), "\\($1\\)");
					processedLine = std::regex_replace(processedLine, std::regex("\\`(.*?)\\`"), "<code>$1</code>");

					section << "<p>" << processedLine << "</p>" << std::endl;
				}
			}
		}
	}



	if (inList) {
		for(int i = 0; i < 100; i ++){
			while(IndentCount[i] != 0){
				section << "</ul>" << std::endl;
				IndentCount[i] --;
			}
		}
	}

	if (inSection) {
		section << "</section>" << std::endl;
		html << section.str();
	}

	// return html.str();

	// *generator toc
	std::stringstream toc;
	if(!h1v.empty()){
		toc << "<ul>";
		for( auto& h1 : h1v ){
			toc << "<li>";
			toc << "<a class=\"toch1\" href=\"#" << h1.name_toc << "\">" << h1.name_real << "</a>";

			if(!h1.h2v.empty()) toc << "<ul>";
			for( auto& h2 : h1.h2v ){
				toc << "<li>";
				toc << "<a class=\"toch2\" href=\"#" << h2.name_toc << "\">" << h2.name_real << "</a>";

				if(!h2.h3v.empty()) toc << "<ul>";
				for( auto& h3 : h2.h3v ){
					toc << "<li>";
					toc << "<a class=\"toch3\" href=\"#" << h3.name_toc << "\">" << h3.name_real << "</a>";
					toc << "</li>";
				}
				if(!h2.h3v.empty()) toc << "</ul>";

				toc << "</li>";
			}
			if(!h1.h2v.empty()) toc << "</ul>";

			toc << "</li>";
		}
		toc << "</ul>";
	}

	// *generate toc js map
	std::stringstream tocjsmap2;
	tocjsmap2 << "const toch2map = {";
	std::stringstream tocjsmap3;
	tocjsmap3 << "const toch3map = {";

	if(!h1v.empty()){
		for( auto& h1 : h1v ){
			for( auto& h2 : h1.h2v ){
				tocjsmap2 << "\'" << h2.name_toc << "\' :{ h1: \'" << h1.name_toc << "\'},";
				for( auto& h3 : h2.h3v ){
					tocjsmap3 << "\'" << h3.name_toc << "\' :{ h1: \'" << h1.name_toc << "\', h2: \'" << h2.name_toc << "\'},";
				}
			}
		}
	}

	tocjsmap2 << "}";
	tocjsmap3 << "}\n" << tocjsmap2.str();

	return {html.str(), toc.str(), tocjsmap3.str()};
}