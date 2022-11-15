#!/bin/bash

fd --type f | sed -e 's/.*\.//' | sed -e 's/.*\///' | sort -u | tail +2 | while read line; do echo "**.$line, "; done
