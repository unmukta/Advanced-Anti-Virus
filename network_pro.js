// Professional network monitoring dashboard
let networkTrafficChart;
let trafficUpdateInterval;

// Initialize professional chart
function initializeProfessionalChart() {
    const ctx = document.getElementById('network-traffic-chart').getContext('2d');
    networkTrafficChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Download (MB/s)',
                    data: [],
                    borderColor: 'rgb(46, 204, 113)',
                    backgroundColor: 'rgba(46, 204, 113, 0.2)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Upload (MB/s)',
                    data: [],
                    borderColor: 'rgb(231, 76, 60)',
                    backgroundColor: 'rgba(231, 76, 60, 0.2)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Real-time Network Traffic',
                    font: { size: 16, weight: 'bold' }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Time'
                    },
                    grid: {
                        display: false
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'MB/s'
                    },
                    beginAtZero: true
                }
            },
            animation: {
                duration: 0
            }
        }
    });
}

// Update chart with real data
async function updateProfessionalChart() {
    try {
        const response = await fetch('/api/network/traffic?limit=30');
        const data = await response.json();
        
        if (data.status === 'success' && data.data.length > 0) {
            const trafficData = data.data;
            const labels = trafficData.map(item => {
                const date = new Date(item.timestamp);
                return date.toLocaleTimeString();
            });
            
            const downloadSpeeds = trafficData.map(item => item.download_speed);
            const uploadSpeeds = trafficData.map(item => item.upload_speed);
            
            networkTrafficChart.data.labels = labels;
            networkTrafficChart.data.datasets[0].data = downloadSpeeds;
            networkTrafficChart.data.datasets[1].data = uploadSpeeds;
            networkTrafficChart.update('none');
            
            // Update speed indicators
            document.getElementById('download-speed').textContent = data.current_speeds.download.toFixed(2);
            document.getElementById('upload-speed').textContent = data.current_speeds.upload.toFixed(2);
        }
    } catch (error) {
        console.error('Failed to update chart:', error);
    }
}

// Professional network scanning
async function startProfessionalScan() {
    const target = document.getElementById('scan-target').value;
    const scanType = document.getElementById('scan-type').value;
    const ports = document.getElementById('scan-ports').value;
    
    if (!target) {
        addNetworkEvent('warning', 'Please enter a scan target');
        return;
    }

    addNetworkEvent('info', 'Starting professional ' + scanType + ' scan on ' + target);
    document.getElementById('scan-progress-container').style.display = 'block';
    document.getElementById('scan-progress').style.width = '0%';

    try {
        // Show scanning animation
        let progress = 0;
        const progressInterval = setInterval(() => {
            progress += 2;
            document.getElementById('scan-progress').style.width = progress + '%';
            if (progress >= 100) clearInterval(progressInterval);
        }, 100);

        const response = await fetch('/api/network/scan?target=' + encodeURIComponent(target) + 
                                   '&scan_type=' + encodeURIComponent(scanType) + 
                                   '&ports=' + encodeURIComponent(ports));
        const data = await response.json();
        
        clearInterval(progressInterval);
        document.getElementById('scan-progress').style.width = '100%';
        
        displayProfessionalScanResults(data);
        addNetworkEvent('success', 'Scan completed: ' + data.results_found + ' hosts found');
        
    } catch (error) {
        addNetworkEvent('error', 'Scan failed: ' + error.message);
    }
    
    setTimeout(() => {
        document.getElementById('scan-progress-container').style.display = 'none';
    }, 1000);
}

// Display professional scan results
function displayProfessionalScanResults(data) {
    const tableBody = document.getElementById('scan-results-table').querySelector('tbody');
    tableBody.innerHTML = '';

    if (data.results && data.results.length > 0) {
        data.results.forEach(host => {
            const row = document.createElement('tr');
            const statusClass = host.status === 'up' ? 'host-up' : 'host-down';
            const statusIcon = host.status === 'up' ? '✓' : '✗';
            
            row.innerHTML = \
                <td>\</td>
                <td><span class="\">\ \</span></td>
                <td>\</td>
                <td>\</td>
                <td>\</td>
                <td>\</td>
                <td>\ms</td>
            \;
            tableBody.appendChild(row);
        });
    } else {
        tableBody.innerHTML = '<tr><td colspan="7" class="text-center">No hosts found</td></tr>';
    }
}

// Load real network connections
async function loadNetworkConnections() {
    try {
        const response = await fetch('/api/network/connections');
        const data = await response.json();
        
        const connectionsContainer = document.getElementById('network-connections');
        connectionsContainer.innerHTML = '';
        
        if (data.connections.length > 0) {
            data.connections.forEach(conn => {
                const connectionElement = document.createElement('div');
                connectionElement.className = 'log-entry';
                connectionElement.innerHTML = \
                    <span class="log-time">[\]</span>
                    <span class="log-info">\ → \ (\)</span>
                \;
                connectionsContainer.appendChild(connectionElement);
            });
        }
    } catch (error) {
        console.error('Failed to load connections:', error);
    }
}

// Initialize professional dashboard
document.addEventListener('DOMContentLoaded', function() {
    console.log('Professional network dashboard initialized');
    initializeProfessionalChart();
    
    // Start real-time updates
    trafficUpdateInterval = setInterval(updateProfessionalChart, 2000);
    setInterval(loadNetworkConnections, 5000);
    
    // Initial load
    updateProfessionalChart();
    loadNetworkConnections();
    addNetworkEvent('info', 'Professional network monitoring initialized');
});

// Cleanup on page unload
window.addEventListener('beforeunload', function() {
    if (trafficUpdateInterval) {
        clearInterval(trafficUpdateInterval);
    }
});
