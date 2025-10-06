# client_examples.ps1
# PowerShell examples for the SoDA DB Workshop demo
# Usage: Start the server (python server_with_db.py), then run this script:
#   .\client_examples.ps1

$BASE = "http://127.0.0.1:8000"

function Post-Student($name, $major, $gpa) {
    $body = @{ name = $name; major = $major; gpa = $gpa } | ConvertTo-Json
    try {
        $resp = Invoke-RestMethod -Uri "$BASE/students" -Method Post -Body $body -ContentType "application/json"
        Write-Host "POST /students ->" ($resp | ConvertTo-Json -Depth 5)
    } catch {
        Write-Host "Error posting student:" $_.Exception.Message -ForegroundColor Red
    }
}

function Get-Students($gpa_min) {
    try {
        $resp = Invoke-RestMethod -Uri "$BASE/students?gpa_min=$gpa_min" -Method Get
        Write-Host "GET /students?gpa_min=$gpa_min ->"
        $resp | ConvertTo-Json -Depth 5
    } catch {
        Write-Host "Error getting students:" $_.Exception.Message -ForegroundColor Red
    }
}

function Raw-Query($gpa_min, [switch]$Unsafe) {
    $unsafeFlag = if ($Unsafe) { "&unsafe=1" } else { "" }
    try {
        $resp = Invoke-RestMethod -Uri "$BASE/raw-query?gpa_min=$gpa_min$unsafeFlag" -Method Get
        if ($Unsafe) {
            Write-Host "GET /raw-query?gpa_min=$gpa_min&unsafe=1 -> (UNSAFE demo)"
        } else {
            Write-Host "GET /raw-query?gpa_min=$gpa_min -> (parameterized)"
        }
        $resp | ConvertTo-Json -Depth 5
    } catch {
        Write-Host "Error on raw-query:" $_.Exception.Message -ForegroundColor Red
    }
}

# ---- Script starts here ----
Write-Host "Running client examples against $BASE" -ForegroundColor Cyan
Write-Host "Make sure server_with_db.py is running." -ForegroundColor Yellow
Write-Host ""

# 1) Insert a sample student
Write-Host "1) Insert a sample student (POST /students)" -ForegroundColor Green
Post-Student -name "Lina Park" -major "AI" -gpa 3.7
Write-Host ""

# 2) List students with gpa >= 3.6
Write-Host "2) List students with gpa >= 3.6 (GET /students)" -ForegroundColor Green
Get-Students -gpa_min 3.6
Write-Host ""

# 3) Show parameterized raw-query (safe)
Write-Host "3) Show parameterized raw-query (safe) (GET /raw-query)" -ForegroundColor Green
Raw-Query -gpa_min 3.6
Write-Host ""

# 4) Show unsafe concatenation demo (do not use in production)
Write-Host "4) Show unsafe concatenation demo (GET /raw-query?unsafe=1) -- for demo only" -ForegroundColor Green
Raw-Query -gpa_min 3.6 -Unsafe
Write-Host ""

Write-Host "Client examples completed." -ForegroundColor Cyan
