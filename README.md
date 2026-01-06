# Asana RL Seed Data Generator

This repository generates a realistic seed dataset simulating an enterprise Asana workspace for reinforcement learning and evaluation of computer-use AI agents.

## Overview

The generator simulates a B2B SaaS company with:
- 150 active users
- Multiple cross-functional teams
- Projects with realistic workflows
- Tasks, subtasks, comments, custom fields, tags, and attachments

The resulting SQLite database mirrors real-world Asana usage patterns and enforces relational and temporal consistency.

## Project Structure

src/
├── main.py # Entry point
├── config.py # Centralized configuration
├── generators/ # Data generation modules
├── utils/ # Utilities (dates, strings, DB, LLM)
output/
└── asana_simulation.sqlite # Generated database

## Setup

pip install -r requirements.txt

## Run

python -m src.main

The generated database will be available at: output/asana_simulation.sqlite

## Notes

LLM-based content generation is optional

All distributions and heuristics are documented in the accompanying design document

Configuration parameters can be adjusted in src/config.py