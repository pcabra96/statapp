-- StatApp launcher
-- Starts the Streamlit server silently in the background,
-- then opens the browser. No Terminal window appears.

set projectPath to "/Users/pablocabramontes/Apps/statapp"
set streamlit to "/Applications/anaconda3/bin/streamlit"
set appURL to "http://localhost:8501"

-- Check if Streamlit is already running on 8501 to avoid double-launching
set alreadyRunning to (do shell script "lsof -ti tcp:8501 | head -1 || true")

if alreadyRunning is "" then
    -- Start Streamlit in the background; redirect output to a log file
    do shell script "PYTHONPATH=" & quoted form of projectPath & " " & quoted form of streamlit & " run " & quoted form of (projectPath & "/app.py") & " > /tmp/statapp.log 2>&1 &"

    -- Wait up to 10 seconds for Streamlit to be ready
    set maxWait to 10
    set waited to 0
    repeat
        delay 1
        set waited to waited + 1
        set ready to (do shell script "lsof -ti tcp:8501 | head -1 || true")
        if ready is not "" then exit repeat
        if waited >= maxWait then exit repeat
    end repeat
end if

-- Open the browser
open location appURL
