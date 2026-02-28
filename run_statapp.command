#!/bin/bash
# run_statapp.command
# Double-click this file to launch StatApp in your browser.

PROJECT=/Users/pablocabramontes/Apps/statapp

# cd to home first — guaranteed to be accessible in any launch context.
# Streamlit calls os.getcwd() on startup; if that directory is restricted
# (which happens when macOS opens a .command file from the Desktop),
# it raises a PermissionError before our app even loads.
cd "$HOME"

# PYTHONPATH lets Python find sections/ and utils/ even though we're not
# running from inside the project folder.
PYTHONPATH="$PROJECT" /Applications/anaconda3/bin/streamlit run "$PROJECT/app.py"
