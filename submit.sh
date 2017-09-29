#!/bin/bash

mkdir job_outputs
rm job_outputs/*
qsub forward_folding.py
