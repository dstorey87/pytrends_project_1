# Ensure script execution halts on errors
$ErrorActionPreference = "Stop"

# Variables
$featureBranch = "feature-blog-generation"
$mainBranch = "main"
$repoPath = "F:\pytrends_project_1"  # Path to your repo

# Navigate to the repository
Write-Host "Navigating to the repository at $repoPath..."
Set-Location -Path $repoPath

# Ensure the repository is clean
Write-Host "Ensuring the repository is clean..."
git status
git add .
git commit -m "WIP: Stabilized blog generation feature" -a

# Push the feature branch
Write-Host "Pushing feature branch '$featureBranch' to remote..."
git push -u origin $featureBranch

# Switch to the main branch
Write-Host "Switching to main branch '$mainBranch'..."
git checkout $mainBranch

# Merge the feature branch into main
Write-Host "Merging '$featureBranch' into '$mainBranch'..."
git merge $featureBranch --no-ff -m "Merge feature-blog-generation into main"

# Push the updated main branch to remote
Write-Host "Pushing main branch to remote..."
git push origin $mainBranch

# Confirm completion
Write-Host "Feature branch '$featureBranch' successfully merged into '$mainBranch'."
