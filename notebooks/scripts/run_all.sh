#!/bin/bash

echo $1
echo $2

LIST_EXPRESSION=$1
CWD=$2

ls $LIST_EXPRESSION | xargs -I _ papermill --cwd $CWD _ _
