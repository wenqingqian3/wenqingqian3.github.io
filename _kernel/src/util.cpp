#include <string>
#include <algorithm>

std::string ltrim(const std::string& str) {
	size_t start = str.find_first_not_of(' ');
	return (start == std::string::npos) ? "" : str.substr(start);
}

std::string rtrim(const std::string& str) {
	size_t end = str.find_last_not_of(' ');
	return (end == std::string::npos) ? "" : str.substr(0, end + 1);
}

std::string trim(const std::string& str) {
	return rtrim(ltrim(str));
}