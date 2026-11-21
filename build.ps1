$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

quarto render notebooks/Analysis.qmd --to all
if ($LASTEXITCODE -ne 0) { throw "quarto render failed" }

Copy-Item -Force notebooks/Analysis.html reports/Analysis.html
Copy-Item -Force notebooks/Analysis.pdf  reports/Analysis.pdf
Remove-Item -Force notebooks/Analysis.html, notebooks/Analysis.pdf
Write-Host "Wrote reports/Analysis.html and reports/Analysis.pdf"
