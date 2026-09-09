#!/bin/bash

# Create the C++ source file
cat > hello.cpp << 'EOF'
#include <iostream>
using namespace std;

int main() {
    cout << "Hello, World!" << endl;
    return 0;
}
EOF

echo "Created hello.cpp"

# Compile the C++ file
g++ -o hello hello.cpp

# Check if compilation was successful
if [ $? -eq 0 ]; then
    echo "Compilation successful! Executable 'hello' created."
    echo "Running the program:"
    ./hello
else
    echo "Compilation failed!"
    exit 1
fi