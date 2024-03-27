#include "algorithms.h"
#include "helpers.h"

Counter::Counter() : one(0), two(0), three(0) {}
void Counter::increment_one() {one++;}
void Counter::increment_two() {two++;}
void Counter::increment_three() {three++;}
void Counter::increment_four() {four++;}
void Counter::print() {std::cout << "One: " << one << " Two: " << two << " Three: " << three << " Four: " << four << std::endl;}

std::map<std::set<std::string>, float> get_transition_information (const std::set<std::string>& state, const std::string& action){

    double state_size = state.size();

    std::map<std::vector<int>, std::set<std::string>> patterns_and_solutions;
    for (const auto& solution : state){
        std::vector<int> pattern = get_coloring(action, solution);
        patterns_and_solutions[pattern].insert(solution);
    }

    std::map<std::set<std::string>, float> transition_info;

    for (const auto& pattern : patterns_and_solutions){
        transition_info[pattern.second] = pattern.second.size() / state_size;
    }

    return transition_info;
}

float v_t(int t, const std::set<std::string>& state, std::map<std::set<std::string>, float>& v_memory, const std::set<std::string>& action_space, const std::set<std::string>& useless_words, Counter& count){

    int state_size = state.size();

    if (t == 4){
        count.increment_four();
    }

    if (t == 3){
        count.increment_three();
    }
    else if (t == 2){
        count.increment_two();
        count.print();
    }
    else if (t == 1){
        count.increment_one();
        count.print();
    }


    if (t == 6 || (t == 5 && state_size > 1)) {return std::numeric_limits<float>::infinity();}
    else if (t == 5) {return 1;}
    else if (state_size == 1) {return 1;}
    else if (state_size == 2) {return 1.5;}
    else if (map_includes_set(v_memory, state)) {return v_memory[state];}

    float state_value = std::numeric_limits<float>::infinity();

    if (t == 0){
        float temp = 1;
        std::map<std::set<std::string>, float> next_states = get_transition_information(state, "salet");

        for (const auto& state : next_states){
                if (state.first.size() == 1 && set_includes_string(state.first, "salet")){continue;}
                else{
                    temp += state.second*v_t(t+1, state.first, v_memory, action_space, useless_words, count);
                }
        }

        state_value = temp;
        
        v_memory[state] = state_value;
        return state_value;

    }

    std::set<std::string> new_useless_words = useless_words; 

    for (const auto& action : action_space) {

        // If the word will provide no information, we do not need to calculate v_t for that word
        // A word will provide no information if the cardinality of the set of possible states we can transition into as a result of chosing that word as an action is 1
        // Formally, |P_t(s_(t+1); s_t, a)| = 1 
        // It is a computational waste to check v_t for these words as they will never be the words that minimie the bellman equation 
        // Additinally, it is slightly more efficient to check useless_words for the string as opposed to new_useless_words, as useless_words 
        // will never be bigger than new_useless_words, and the words in new_useless_words that are not in useless_words have already been iterated 
        // through in this function call. 
        // Not sure if this is actually faster however, as we need to create a new set for every function call 
        // However, my current rationale is that each word in the useless_words set reduces the number of times you need to call get_transition_information by 1.
        if (set_includes_string(useless_words, action)){
            continue;
        }


        else{
            float temp = 1;
            std::map<std::set<std::string>, float> next_states = get_transition_information(state, action);

            // If the number of possible states as a result of choosing some word as an action is 1, this means that the resulting state, s_(t+1) is equal to the original state
            // s_t. Clearly this guess provides no information, and will therefore never be the action that minimizes the bellman equation. 
            if (next_states.size() == 1) {
                new_useless_words.insert(action);
                continue;}

            // Lowerbounding V_t for some action, the paper does a great job of explaining why this is an appropriate lowerbound, so I won't go into it here. However, the idea
            // is to lowerbound V_t for some action, and if that lowerbound is still greater than the current state value, then we can prune the action, as it will never result 
            // in a lower state value than what we already have. 
            for (const auto& state : next_states){

                // Lowerbounding p_t(s_(t+1) | s_t, a)*V_(t+1)(s_(t+1))
                temp += state.second*((2*state.first.size()-1) / state.first.size());
            }

            // If the lower bound is less than the current state value, then we need to actually evaluate v_t for some action a, which we do in this block of code 
            if (temp < state_value){
                temp = 1;
                for (const auto& state : next_states){
                    if (state.first.size() == 1 && set_includes_string(state.first, action)){continue;}
                    else{
                        temp += state.second*v_t(t+1, state.first, v_memory, action_space, new_useless_words, count);
                    }
                }

                if (temp < state_value) {state_value = temp;}
            }
        }
        

    }


    v_memory[state] = state_value;
    return state_value;
}