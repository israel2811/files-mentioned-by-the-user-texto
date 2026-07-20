# Script de Optimización de Recursos de NEXUS
# Regla de Usuario #3: Reducir prioridad de Google Drive, OneDrive y Dropbox.
# Este script busca los procesos de sincronización activos y reduce su prioridad a "Idle".

$processNames = @("googledrivesync", "OneDrive", "Dropbox", "GoogleDriveFS")

Write-Host "Iniciando optimización de procesos de sincronización..." -ForegroundColor Cyan

foreach ($name in $processNames) {
    $processes = Get-Process -Name $name -ErrorAction SilentlyContinue
    
    if ($processes) {
        foreach ($proc in $processes) {
            # Cambiar prioridad base a Idle (Baja)
            if ($proc.PriorityClass -ne 'Idle') {
                try {
                    $proc.PriorityClass = [System.Diagnostics.ProcessPriorityClass]::Idle
                    Write-Host "[+] Prioridad de $($proc.Name) (PID: $($proc.Id)) ajustada a 'Idle'." -ForegroundColor Green
                } catch {
                    Write-Host "[-] No se pudo ajustar la prioridad de $($proc.Name). Intenta ejecutar como Administrador." -ForegroundColor Red
                }
            } else {
                Write-Host "[i] El proceso $($proc.Name) (PID: $($proc.Id)) ya está en prioridad 'Idle'." -ForegroundColor Yellow
            }
        }
    } else {
        Write-Host "[-] Proceso de sincronización '$name' no encontrado en ejecución." -ForegroundColor Gray
    }
}

Write-Host "Optimización completada. La CPU y la RAM de tu PC ahora están priorizadas para tus flujos de trabajo locales." -ForegroundColor Cyan
