#!/bin/bash
head -c $((256 * 256 * 2)) /dev/urandom | xxd -c $((256 * 2)) -ps
