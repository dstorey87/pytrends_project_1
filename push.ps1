# Ensure script execution halts on errors
$ErrorActionPreference = "Stop"

# Variables
$currentBranch = "feature-efficient-model-server"  # Replace with your current feature branch
$mainBranch = "main"
$repoPath = "F:\pytrends_project_1"  # Path to your repo

# Navigate to the repository
Write-Host "Navigating to the repository at $repoPath..."
Set-Location -Path $repoPath

# Ensure all changes are staged and committed
Write-Host "Staging and committing changes..."
git add .
git commit -m "WIP: Stabilized blog generation feature" -a

# Push the current feature branch
Write-Host "Pushing current feature branch '$currentBranch' to remote..."
git push -u origin $currentBranch

# Switch to the main branch
Write-Host "Switching to main branch '$mainBranch'..."
git checkout $mainBranch

# Merge the feature branch into main
Write-Host "Merging '$currentBranch' into '$mainBranch'..."
git merge $currentBranch --no-ff -m "Merge $currentBranch into $mainBranch"

# Push the updated main branch to remote
Write-Host "Pushing main branch to remote..."
git push origin $mainBranch

# Confirm completion
Write-Host "Feature branch '$currentBranch' successfully merged into '$mainBranch'."
