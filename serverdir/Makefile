.PHONY: cExe cppExe ALL
SHELL := /bin/bash

# Daca ARCHITECTURE nu e pasat la rulare, punem o valoare default (ex: 1)
ARCHITECTURE ?= 1

CFLAGS = -g
CXX_FLAGS = -std=c++20 -g

ifeq ($(ARCHITECTURE), 2)
    CC  = gcc-aarch64-linux-gnu
    CXX = g++-aarch64-linux-gnu
else ifeq ($(ARCHITECTURE), 3)
    CC  = gcc-13-aarch64-linux-gnu-base
    CXX = g++-12-aarch64-linux-gnu
else
    CC  = gcc
    CXX = g++
endif

ALL: cExe cppExe

cExe:
	$(CC) $(CFLAGS) *.c -o exeC

cppExe:
	$(CXX) $(CXX_FLAGS) *.cpp -o exeCpp