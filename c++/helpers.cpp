#include "helpers.h"

bool string_includes_char(const std::string& str, char ch){
    return str.find(ch) != std::string::npos;
}


std::vector<int> get_coloring(const std::string& action, const std::string& solution){
    std::vector<int> pattern;
    std::unordered_map<char, int> max_yellows;

    for (int i = 0; i < solution.length(); i++) {
        if (solution[i] != action[i]) {max_yellows[solution[i]] += 1;}
    }


    for (int i = 0; i < solution.length(); i++) {

        // Green 
        if (action[i] == solution[i]) {pattern.push_back(2);}

        // Yellow or Gray 
        else if (action[i] != solution[i] && string_includes_char(solution, action[i])){
            if (max_yellows[action[i]] > 0){
                pattern.push_back(1);
                max_yellows[action[i]] -= 1;
            }
            else{
                pattern.push_back(0);
            }
        }

        // Gray 
        else {pattern.push_back(0);}
    }

    return pattern;
}

bool map_includes_set(const std::map<std::set<std::string>, float>& m, const std::set<std::string>& s){
    if (m.find(s) == m.end()) {return false;}
    return true; 
}

bool set_includes_string(const std::set<std::string>& s, const std::string& str){
    return s.find(str) != s.end();
}

std::set<std::string> read_text_file(const std::string& file_path){
    std::ifstream input_file(file_path);

    std::set<std::string> return_set;

    std::string line;

    if (!input_file.is_open()){
        return return_set;
    }

    while (std::getline(input_file, line)){
        return_set.insert(line);
    }

    input_file.close();

    return return_set;
}
