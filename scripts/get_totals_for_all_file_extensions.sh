#!/bin/bash

fd --type f | sed -e 's/.*\.//' | sed -e 's/.*\///' | sort | uniq -c | sort -rn
