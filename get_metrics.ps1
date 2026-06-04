# PowerShell script to integrate with Python system monitoring
$pythonScript = @"
from core.monitor import get_system_metrics
metrics = get_system_metrics()
import json
print(json.dumps(metrics))
"@

# Run the Python script and capture output
$output = python -c $pythonScript 2>&1

# Parse the JSON output
try {
    $metrics = $output | ConvertFrom-Json
    Write-Host "System Metrics:"
    Write-Host "CPU Usage: $($metrics.cpu_usage)%"
    Write-Host "Memory Usage: $($metrics.memory_usage)%"
    Write-Host "Disk Usage: $($metrics.disk_usage)%"
    Write-Host "Network Sent: $($metrics.network_sent_mb) MB/s"
    Write-Host "Network Received: $($metrics.network_recv_mb) MB/s"
    
    Write-Host "`nTop Processes:"
    $metrics.top_processes | ForEach-Object {
        Write-Host "  $($_.name) (PID: $($_.pid)) - CPU: $($_.cpu_percent)%, Memory: $($_.memory_percent)%"
    }
} catch {
    Write-Host "Error parsing metrics: $($_.Exception.Message)"
    Write-Host "Raw output: $output"
}
