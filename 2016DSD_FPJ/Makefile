CXX=g++
CXXFLAGS=-std=c++11
.PHONY: clean remake test1 test2 test3 test4

sdt: sdt.o qm.o
	$(CXX) $(CXXFLAGS) sdt.o qm.o -o sdt
sdt.o: state_diagram_translator.cpp qm.o
	$(CXX) $(CXXFLAGS) -c state_diagram_translator.cpp -o sdt.o
qm.o: quine_mc_cluskey.cpp
	$(CXX) $(CXXFLAGS) -c quine_mc_cluskey.cpp -o qm.o
clean:
	rm *.o sdt
remake:
	make clean
	make
test1:
	./sdt < test1.in
test2:
	./sdt < test2.in
test3:
	./sdt < test3.in
test4:
	./sdt < test4.in
