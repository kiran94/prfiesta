#!/bin/bash

LIST_EXPRESSION=$1
CWD=$2

ls $LIST_EXPRESSION | xargs -I _ papermill --cwd $CWD _ _
