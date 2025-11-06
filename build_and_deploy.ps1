# D2CasualSP Build and Deploy Script
# This script generates the mod, copies it to D2R, and launches the game

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "D2CasualSP Build and Deploy" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Generate mod files
Write-Host "[1/3] Generating mod files..." -ForegroundColor Yellow
.\.venv\Scripts\python.exe main.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "  Success: Mod files generated" -ForegroundColor Green
} else {
    Write-Host "  Error: Failed to generate mod files" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Step 2: Copy to D2R mods directory
Write-Host "[2/3] Copying to Diablo 2 Resurrected..." -ForegroundColor Yellow

# Hardcoded paths - adjust these to match your installation
$D2R_MODS_PATH = "C:\Program Files (x86)\Diablo II Resurrected\mods"
$SOURCE_PATH = ".\results\D2RCasualSP"

# Create mods directory if it doesn't exist
if (-not (Test-Path $D2R_MODS_PATH)) {
    New-Item -ItemType Directory -Path $D2R_MODS_PATH -Force | Out-Null
    Write-Host "  Created mods directory" -ForegroundColor Gray
}

# Copy the mod
Copy-Item -Path $SOURCE_PATH -Destination $D2R_MODS_PATH -Recurse -Force

if ($?) {
    Write-Host "  Success: Mod copied to $D2R_MODS_PATH" -ForegroundColor Green
} else {
    Write-Host "  Error: Failed to copy mod files" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Step 3: Launch Diablo 2 Resurrected
Write-Host "[3/3] Launching Diablo 2 Resurrected..." -ForegroundColor Yellow

# Hardcoded D2R executable path - adjust to match your installation
$D2R_EXE = "C:\Program Files (x86)\Diablo II Resurrected\D2R.exe"

if (Test-Path $D2R_EXE) {
    Start-Process $D2R_EXE -ArgumentList "-mod D2RCasualSP -txt"
    Write-Host "  Success: Game launched with D2RCasualSP mod" -ForegroundColor Green
} else {
    Write-Host "  Error: D2R executable not found at $D2R_EXE" -ForegroundColor Red
    Write-Host "  Please update the path in the script" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Done! Enjoy your modded game!" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
