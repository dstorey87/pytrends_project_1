# Define the base directory to scan
$modelsBasePath = "F:\models"

# Define the output file path
$outputFilePath = "F:\pytrends_project_1\all_files_and_folders.txt"

# Check if the base directory exists
if (-Not (Test-Path $modelsBasePath)) {
    Write-Host "The base directory does not exist: $modelsBasePath" -ForegroundColor Red
    exit
}

# Ensure the output directory exists
$outputDir = Split-Path -Path $outputFilePath
if (-Not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

# Perform a recursive listing of all files and folders
Get-ChildItem -Path $modelsBasePath -Recurse -Force | Select-Object -ExpandProperty FullName | Out-File -FilePath $outputFilePath -Encoding UTF8

# Confirmation message
Write-Host "Recursive file and folder listing saved to $outputFilePath" -ForegroundColor Green
