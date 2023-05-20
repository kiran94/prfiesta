#!/bin/bash

ls *.ipynb | xargs -I _ papermill _ _
