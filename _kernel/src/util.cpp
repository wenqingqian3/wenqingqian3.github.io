#include <string>
#include <algorithm>

std::string ltrim(const std::string& str) {
	size_t start = str.find_first_not_of(' ');
	return (start == std::string::npos) ? "" : str.substr(start);
}