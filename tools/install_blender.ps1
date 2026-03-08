$ErrorActionPreference = "Stop"

$url = "https://download.blender.org/release/Blender4.2/blender-4.2.0-windows-x64.zip"
$toolsDir = "D:\Blender\blenderscripts\tools"
$zipPath = Join-Path $toolsDir "blender.zip"
$extractPath = $toolsDir
$finalBlenderDir = Join-Path $toolsDir "blender"

# Ensure tools directory exists
if (-not (Test-Path $toolsDir)) {
    New-Item -ItemType Directory -Force -Path $toolsDir | Out-Null
}

# Remove existing blender directory if it exists to avoid conflicts
if (Test-Path $finalBlenderDir) {
    Write-Host "Removendo instalação anterior do Blender..."
    Remove-Item $finalBlenderDir -Recurse -Force
}

Write-Host "1/4: Iniciando o download do Blender 4.2 LTS Portable (isso pode levar alguns minutos)..."
Invoke-WebRequest -Uri $url -OutFile $zipPath

Write-Host "2/4: Extraindo os arquivos..."
# Usando tar que é nativo no Windows 10/11 e muito mais rápido que Expand-Archive
tar -xf $zipPath -C $extractPath

Write-Host "3/4: Removendo o arquivo .zip para economizar espaço..."
Remove-Item $zipPath -Force

Write-Host "4/4: Organizando a pasta..."
# O tar extrai para uma pasta chamada "blender-4.2.0-windows-x64" geralmente. Vamos renomear para "blender"
$extractedFolder = Join-Path $extractPath "blender-4.2.0-windows-x64"
if (Test-Path $extractedFolder) {
    Rename-Item -Path $extractedFolder -NewName "blender" -Force
}

Write-Host ""
Write-Host "✅ SUCESSO! Blender 4.2 LTS instalado em modo portátil."
Write-Host "Caminho: $finalBlenderDir\blender.exe"
