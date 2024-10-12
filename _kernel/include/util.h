#pragma once

#include <string>
#include <algorithm>

inline std::string ltrim(const std::string& str) {
	size_t start = str.find_first_not_of(' ');
	return (start == std::string::npos) ? "" : str.substr(start);
}

inline std::string rtrim(const std::string& str) {
	size_t end = str.find_last_not_of(' ');
	return (end == std::string::npos) ? "" : str.substr(0, end + 1);
}

inline std::string trim(const std::string& str) {
	return rtrim(ltrim(str));
}

inline std::string convert_udl_to_space(const std::string& str) {
    std::string res = str;
    for(auto& c: res){
        if(c == '_') c = ' ';
    }
    return res;
}