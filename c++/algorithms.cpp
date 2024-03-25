#include "algorithms.h"
#include "helpers.h"


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

float v_t(int t, const std::set<std::string>& state, std::map<std::set<std::string>, float>& v_memory, const std::set<std::string>& action_space){

    int state_size = state.size();

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
                    temp += state.second*v_t(t+1, state.first, v_memory, action_space);
                }
        }

        state_value = temp;
        
        v_memory[state] = state_value;
        return state_value;

    }

    for (const auto& action : action_space) {
        float temp = 1;
        std::map<std::set<std::string>, float> next_states = get_transition_information(state, action);
        if (next_states.size() == 1) {continue;}

        // Lowerbounding V_t for some action 
        for (const auto& state : next_states){

            // Lowerbounding p_t(s_(t+1) | s_t, a)*V_(t+1)(s_(t+1))
            temp += state.second*((2*state.first.size()-1) / state.first.size());
        }

        if (temp < state_value){
            temp = 1;
            for (const auto& state : next_states){
                if (state.first.size() == 1 && set_includes_string(state.first, action)){continue;}
                else{
                    temp += state.second*v_t(t+1, state.first, v_memory, action_space);
                }
            }

            if (temp < state_value) {state_value = temp;}
        }

    }


    v_memory[state] = state_value;
    return state_value;
}