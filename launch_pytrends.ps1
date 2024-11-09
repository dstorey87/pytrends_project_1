# Set up variables
$wslDistro = "Ubuntu" # Replace with your WSL distribution name if it's not "Ubuntu"
$projectPathWindows = "F:\pytrends_project_1"
$projectPathWSL = "/mnt/f/pytrends_project_1"
$venvPathWSL = "/mnt/f/pytrends_project_1/pytrends_env"

# Launch WSL and navigate to the project directory
wsl.exe -d $wslDistro bash -c "
cd $projectPathWSL &&
if [ ! -d $venvPathWSL ]; then
    python3 -m venv $venvPathWSL &&
    echo 'Virtual environment created.'
fi &&
source $venvPathWSL/bin/activate &&
echo 'Environment activated.' &&
exec bash
"
