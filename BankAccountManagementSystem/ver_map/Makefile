CPPFLAGS = -std=c++11 -O2 -Wall -Wextra
COMPILER = g++-4.8

.PHONY: clean all remake

all: final_project

final_project:  nextWord.o history.o clientMap_Map.o md5cstr.o main.o ID_table.o wildcard.o
	$(COMPILER) $(CPPFLAGS) nextWord.o history.o clientMap_Map.o md5cstr.o main.o ID_table.o wildcard.o -o $@

nextWord.o: nextWord.h nextWord.cpp
	$(COMPILER) $(CPPFLAGS) -c nextWord.cpp -o $@  

history.o: history.h history.cpp
	$(COMPILER) $(CPPFLAGS) -c history.cpp -o $@  

clientMap_Map.o: clientMap_Map.h clientMap_Map.cpp
	$(COMPILER) $(CPPFLAGS) -c clientMap_Map.cpp -o $@

md5cstr.o: md5cstr.h md5cstr.cpp
	$(COMPILER) $(CPPFLAGS) -c md5cstr.cpp -o $@

ID_table.o: ID_table.h ID_table.cpp
	$(COMPILER) $(CPPFLAGS) -c ID_table.cpp -o $@

wildcard.o: wildcard.h wildcard.cpp
	$(COMPILER) $(CPPFLAGS) -c wildcard.cpp -o $@

main.o: main.cpp
	$(COMPILER) $(CPPFLAGS) -c main.cpp -o $@

run:	
	./final_project < release_data/test_in_small.txt > out

clean:
	rm -rf *.o final_project *~ out

remake: clean all
