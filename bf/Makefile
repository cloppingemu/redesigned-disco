CFLAGS = -O2 -Wall -Wextra -fpic

OBJS += bf.o

LIBNAME=libbf
DYLIBSUFFIX=so
STLIBSUFFIX=a

DYLIBNAME=$(LIBNAME).$(DYLIBSUFFIX)
STLIBNAME=$(LIBNAME).$(STLIBSUFFIX)

all: $(DYLIBNAME) $(STLIBNAME) interface

$(OBJS): %.o: %.c libbf.h
	@echo "\nMaking $(OBJS) using $<"
	cc -o $*.o -c $< $(CFLAGS)

$(DYLIBNAME): bf.o
	@echo "\nMaking $(DYLIBNAME) using $^"
	cc -shared -o $(DYLIBNAME) $^

$(STLIBNAME): bf.o
	@echo "\nMaking $*"
	ar rcs $(STLIBNAME)

lib: $(DYLIBNAME) $(STLIBNAME)

interface/bfi.o: interface/%.o: interface/%.c
	@echo "\nMaking $*.o using $<"
	cc -o interface/$*.o -c $< $(CFLAGS)

interface/bfi.out: interface/bfi.o
	@echo "\nMaking $*.out using $^"
	cc -o $*.out $(CFLAGS) $^

interface: interface/bfi.out

clean:
	@echo "\nCleaning\n"
	rm -Rf ../env
	rm -f *.o *.so *.out *.a interface/*.o interface/*.out
	rm -f MANIFEST pkg/bf/* pkg/README.md pkg/bf*.tar.gz pkg/bf*.whl
	rm -Rf build dist pkg/dist pkg/build pkg/*.egg-info

env:
	@echo "\nSetting up environment"
	virtualenv ../env
	../env/bin/python -m pip install -r ../requirements.txt

build: env
	@echo "\nSetting up Python Wheel"
	cp __init__.py pkg/bf/__init__.py
	cp libbf.so pkg/bf/libbf.so
	../env/bin/python -m build pkg -o pkg -w

install: build
	@echo "\nInstall python package"
	../env/bin/python -m pip install pkg/bf*.whl
