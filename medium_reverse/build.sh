#!/bin/bash
g++ keygen.cpp -m32 -o bin/keygen
g++ validator.cpp -m32 -o bin/validator && strip bin/validator
