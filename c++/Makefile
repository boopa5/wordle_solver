CXX_FLAGS = -std=c++23 -g

all: main

main: algorithms.o helpers.o main.o
	g++ $(CXX_FLAGS) -O3 -o main helpers.o algorithms.o main.o

main.o: main.cpp
	g++ $(CXX_FLAGS) -O3 -c main.cpp

helpers.o: helpers.cpp
	g++ $(CXX_FLAGS) -c helpers.cpp

algorithms.o: algorithms.cpp
	g++ $(CXX_FLAGS) -O3 -c algorithms.cpp

clean: 
	rm -f main *.o