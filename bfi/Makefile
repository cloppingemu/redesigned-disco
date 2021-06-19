CFLAGS = -O2 -Wall -Wextra -fpic

OBJS += bf.o

LIBNAME=libbf
DYLIBSUFFIX=so
STLIBSUFFIX=a

DYLIBNAME=$(LIBNAME).$(DYLIBSUFFIX)
STLIBNAME=$(LIBNAME).$(STLIBSUFFIX)

all: $(DYLIBNAME) interface build

$(OBJS): %.o: %.c
	@echo "\nMaking $(OBJS) using $<"
	cc -o $*.o -c $< $(CFLAGS)

$(DYLIBNAME): bf.o
	@echo "\nMaking $(DYLIBNAME) using $^"
	cc -shared -o $(DYLIBNAME) $^

$(STLIBNAME): bf.o
	@echo "\nMaking $*"
	ar rcs $(STLIBNAME)

lib: $(DYLIBNAME) $(STLIBNAME)

interface/bfi.o: interface/%.o: interface/%.c $(DYLIBNAME)
	@echo "\nMaking $*.o using $<"
	cc -o interface/$*.o -c $< $(CFLAGS) -I$(realpath .)

interface/bfi.out:  interface/%.out: interface/%.o
	@echo "\nMaking $*.out using $^"
	#export LD_LIBRARY_PATH=$(realpath .)
	cc -o interface/$*.out $(CFLAGS) $^ -L$(realpath .) -lbf

interface: interface/bfi.out

interface-rpath: interface/bfi.o
	@echo "\nMaking interface/bfi.out using $^ with rpath"
	cc -L$(realpath .) -Wl,-rpath=$(realpath .) -Wall -o interface/bfi.out interface/bfi.o -lbf

env:
	@echo "\nSetting up environment"
	virtualenv ../env
	../env/bin/python -m pip install -r ../requirements.txt

build: env $(DYLIBNAME)
	@echo "\nSetting up Python Wheel"
	cp __init__.py pkg/bfi/__init__.py
	cp libbf.so pkg/bfi/libbf.so
	../env/bin/python -m build pkg -o pkg -w

install: build
	@echo "\nInstall python package"
	../env/bin/python -m pip install pkg/bfi*.whl

clean: clean-pkg clean-env clean-lib clean-interface
	@echo "Cleaned\n"

clean-c: clean-interface clean-lib
clean-python: clean-env clean-pkg

clean-lib:
	rm -f *.o *.so *.out *.a

clean-interface:
	rm -f interface/*.o interface/*.out

clean-env:
	rm -Rf ../env

clean-pkg:
	rm -f pkg/bfi/* pkg/README.md pkg/bfi*.tar.gz pkg/bfi*.whl
	rm -Rf build dist pkg/dist pkg/build pkg/*.egg-info
