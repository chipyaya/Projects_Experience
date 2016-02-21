CPPFLAGS = -std=c++11 -O3
COMPILER = g++

.PHONY: clean all remake

all: final_project

final_project:  nextWord.o history.o clientMap.o md5cstr.o main.o wildcard.o
	$(COMPILER) $(CPPFLAGS) nextWord.o history.o clientMap.o md5cstr.o main.o wildcard.o -o $@

nextWord.o: nextWord.h nextWord.cpp
	$(COMPILER) $(CPPFLAGS) -c nextWord.cpp -o $@  

history.o: history.h history.cpp
	$(COMPILER) $(CPPFLAGS) -c history.cpp -o $@  

clientMap.o: clientMap.h clientMap.cpp
	$(COMPILER) $(CPPFLAGS) -c clientMap.cpp -o $@

md5cstr.o: md5cstr.h md5cstr.cpp
	$(COMPILER) $(CPPFLAGS) -c md5cstr.cpp -o $@


wildcard.o: wildcard.h wildcard.cpp
	$(COMPILER) $(CPPFLAGS) -c wildcard.cpp -o $@

main.o: main.cpp
	$(COMPILER) $(CPPFLAGS) -c main.cpp -o $@

run:	
	/final_project 

clean:
	rm -rf *.o final_project *~ out

remake: clean all
