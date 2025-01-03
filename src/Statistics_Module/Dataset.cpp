#include "../../include/Statistics_Module/Dataset.hpp"
#include "../../include/Statistics_Module/Utils.hpp"
#include <algorithm>
#include <stdexcept>

namespace ScientificToolbox::Statistics {

// Constructor implementation
Dataset::Dataset(const std::vector<std::unordered_map<std::string, OptionalDataValue>>& inputData) : data(inputData) {
    if (data.empty()) {
        throw std::runtime_error("Cannot create dataset from empty data");
    }
}

// Column names getter
std::vector<std::string> Dataset::getColumnNames() const {
    if (data.empty()) {
        return {};
    }
    
    std::vector<std::string> names;
    for (const auto& [key, _] : data[0]) {
        names.push_back(key);
    }
    return names;
}

// Add new row
void Dataset::addRow(const std::unordered_map<std::string, OptionalDataValue>& row) {
    // Verify row has same columns as existing data
    if (!data.empty()) {
        for (const auto& [key, _] : data[0]) {
            if (row.find(key) == row.end()) {
                throw std::runtime_error("New row missing column: " + key);
            }
        }
    }
    data.push_back(row);
}

// Template specialization for numeric types
template<typename T>
std::vector<T> Dataset::getColumn(const std::string& columnName) const {
    return Utils::extractColumn<T>(data, columnName);
}

// Explicit template instantiations
template std::vector<int> Dataset::getColumn<int>(const std::string&) const;
template std::vector<double> Dataset::getColumn<double>(const std::string&) const;
template std::vector<std::string> Dataset::getColumn<std::string>(const std::string&) const;

// Iterator implementation is in header file since it's template-based

} // namespace ScientificToolbox::Statistics