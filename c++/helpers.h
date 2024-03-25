#ifndef HELPERS_H
#define HELPERS_H

#include <set>
#include <map>
#include <string>
#include <vector> 
#include <iostream>
#include <unordered_map>
#include <fstream>
#include <iostream>



bool string_includes_char(const std::string& str, char ch);
bool map_includes_set(const std::map<std::set<std::string>, float>& m, const std::set<std::string>& s);
bool set_includes_string(const std::set<std::string>& s, const std::string& str);
std::vector<int> get_coloring(const std::string& action, const std::string& solution);
std::set<std::string> read_text_file(const std::string& file_path);



#endif // HELPERS_H