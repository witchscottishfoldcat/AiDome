# Makefile for the ArkHeart Project
# ---------------------------------
# This file provides convenient shortcuts for common development tasks.
# Usage:
#   make [target]
#
# Example:
#   make run-brain
# ---------------------------------

# Define variables
PYTHON_INTERP = poetry run python
GODOT_PATH = body_godot
GODOT_EXEC = godot # Assumes 'godot' is in your system's PATH. Adjust if necessary.

# Phony targets are commands that don't produce a file with the same name.
.PHONY: help install run-brain run-body

help:
	@echo "Available commands:"
	@echo "  install        - Installs all Python dependencies from poetry.lock."
	@echo "  run-brain      - Starts the Brain service (FastAPI) in auto-reload mode."
	@echo "  run-body       - Opens the Body project (Godot) in the editor."

install:
	@echo "--> Installing Python dependencies via Poetry..."
	@poetry install

run-brain:
	@echo "--> Starting Brain service on http://127.0.0.1:8000"
	@poetry run uvicorn app.main:app --reload

run-body:
	@echo "--> Opening Godot editor for the Body project..."
	@$(GODOT_EXEC) --path $(GODOT_PATH)