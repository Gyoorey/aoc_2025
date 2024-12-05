// AI generated translation from sol.py

#include <iostream>
#include <fstream>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <sstream>

using namespace std;

int part1(const unordered_map<int, vector<int>>& rules, const vector<vector<int>>& updates) {
    int sum = 0;
    for (const auto& update : updates) {
        bool valid = true;
        for (size_t i = 0; i < update.size(); ++i) {
            for (size_t j = i + 1; j < update.size(); ++j) {
                if (rules.at(update[j]).end() != find(rules.at(update[j]).begin(), rules.at(update[j]).end(), update[i])) {
                    valid = false;
                    break;
                }
            }
            if (!valid) break;
        }
        if (valid) {
            sum += update[update.size() / 2];
        }
    }
    return sum;
}

int part2(const unordered_map<int, vector<int>>& rules, const vector<vector<int>>& original_updates) {
    vector<vector<int>> sorted_updates = original_updates;
    for (auto& update : sorted_updates) {
        sort(update.begin(), update.end(), [&rules](int x, int y) {
            if (rules.find(x) != rules.end() && find(rules.at(x).begin(), rules.at(x).end(), y) != rules.at(x).end()) {
                return true;
            }
            return false;
        });
    }
    return part1(rules, sorted_updates) - part1(rules, original_updates);
}

pair<int, int> solve(const string& input) {
    ifstream file(input);
    string line;
    vector<pair<int, int>> pairs;
    vector<vector<int>> updates;
    unordered_map<int, vector<int>> rules;

    while (getline(file, line) && !line.empty()) {
        stringstream ss(line);
        string token;
        vector<int> pair;
        while (getline(ss, token, '|')) {
            pair.push_back(stoi(token));
        }
        pairs.emplace_back(pair[0], pair[1]);
    }

    for (const auto& p : pairs) {
        rules[p.first].push_back(p.second);
    }

    while (getline(file, line)) {
        stringstream ss(line);
        string token;
        vector<int> update;
        while (getline(ss, token, ',')) {
            update.push_back(stoi(token));
        }
        updates.push_back(update);
    }

    return {part1(rules, updates), part2(rules, updates)};
}

int main() {
    string input = "input.txt";
    auto result = solve(input);
    cout << "Part 1: " << result.first << endl;
    cout << "Part 2: " << result.second << endl;
    return 0;
}