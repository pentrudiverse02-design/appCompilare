.PHONY: cBin cExe
SHELL := bash
CC = gccCFLAGS
CFLAGS = -g
fisiereC := $(wildcard *.c)
fisiereH := $(wildcard *.h)
fisiereO := $(wildcard *.o)

cExe: cBin
cBin:
	mkdir binare &&\
	for  i in /[*.o] ; do mv $i binare done
%.o : %.c
	$(CC) -c $(CFLAGS) $< -o $@
