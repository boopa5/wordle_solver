#ifndef ALGORITHMS_H
#define ALGORITHMS_H

#include <set>
#include <map>
#include <string>
#include <vector> 
#include <iostream>
#include <unordered_map>
#include <limits> 
#include <unordered_set>

class Counter{
    private:
        int one;
        int two;
        int three;
        int four; 

    public:
        Counter();
        void increment_one();
        void increment_two();
        void increment_three();
        void increment_four();
        void print();
};


std::map<std::set<std::string>, float> get_transition_information (const std::set<std::string>& state, const std::string& action);
float v_t(int t, const std::set<std::string>& state, std::map<std::set<std::string>, float>& v_memory, const std::set<std::string>& action_space, const std::set<std::string>& useless_words, Counter& count);


#endif // ALGORITHMS_H