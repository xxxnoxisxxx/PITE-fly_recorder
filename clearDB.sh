#!/bin/bash

rm -f $1
sqlite3 $1 ''
chmod 777 $1