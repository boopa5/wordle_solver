CXX_FLAGS = -std=c++11 -g

all: main

main: algorithms.o helpers.o main.o
	g++ $(CXX_FLAGS) -o main helpers.o algorithms.o main.o

main.o: main.cpp
	g++ $(CXX_FLAGS) -c main.cpp

helpers.o: helpers.cpp
	g++ $(CXX_FLAGS) -c helpers.cpp

algorithms.o: algorithms.cpp
	g++ $(CXX_FLAGS) -c algorithms.cpp

clean: 
	rm -f main *.o