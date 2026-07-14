#!/usr/bin/env bash

if [[ -n "$1" ]]
then
  python3 -m serverdir.server -port $1
else
  python3 -m serverdir.server
fi