#include "algorithms.h"
#include "helpers.h"

int main(){
    std::set<std::string> answer_list = read_text_file("../text_files/answer_list.txt");
    std::set<std::string> action_space = read_text_file("../text_files/word_list.txt");
    
    std::map<std::set<std::string>, float> mem;
    Counter count;
    std::set<std::string> useles_words;

    float expected_value = v_t(0, answer_list, mem, action_space, useles_words, count);
    std::cout << expected_value;


}