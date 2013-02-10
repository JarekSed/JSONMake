COMPILER = gcc
CCFLAGS  = -Wall -O2 -lm
 
all: geometry

geometry: geometry.o
	$(COMPILER) $(CCFLAGS) -o geometry geometry.o
geometry.o: geometry.c
	$(COMPILER) $(CCFLAGS) -c geometry.c

clean:
	rm -f geometry
	rm -f *.o

