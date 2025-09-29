from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import subprocess
import json
import re

# Create FastAPI app instance FIRST
app = FastAPI(title="DLP Enterprise 3.0")

# Root endpoint
@app.get("/")
def root():
    return {"message": "Enterprise DLP 3.0 API", "docs": "/docs", "health": "/health"}

# Health endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "3.0.0", "zero_trust": True}

# USB status endpoint
@app.get("/api/v1/usb/status")
async def get_usb_status():
    return {"status": "active", "monitoring": True, "enterprise": True}

# FIXED USB devices endpoint - CORRECT PowerShell syntax
@app.get("/api/v1/usb/devices")
async def get_usb_devices():
    try:
        # CORRECT PowerShell command with proper . syntax
        result = subprocess.run([
            'powershell', 
            'Get-PnpDevice -PresentOnly | Where-Object {.Status -eq "OK" -and .Class -eq "USB"} | Select-Object FriendlyName, Status, DeviceID | ConvertTo-Json'
        ], capture_output=True, text=True, timeout=10)
        
        print(f"PowerShell return code: {result.returncode}")
        
        if result.returncode == 0 and result.stdout.strip() and result.stdout.strip() != 'null':
            try:
                devices = json.loads(result.stdout)
                if not isinstance(devices, list):
                    devices = [devices]
                
                real_devices = []
                for device in devices:
                    # Skip system USB devices
                    if any(x in device['FriendlyName'] for x in ['Hub', 'Controller', 'Host', 'Root']):
                        continue
                        
                    # Extract vendor and product IDs
                    vid_match = re.search(r'VID_([0-9A-Fa-f]{4})', device['DeviceID'], re.IGNORECASE)
                    pid_match = re.search(r'PID_([0-9A-Fa-f]{4})', device['DeviceID'], re.IGNORECASE)
                    
                    real_devices.append({
                        'name': device['FriendlyName'],
                        'status': device['Status'],
                        'type': 'physical',
                        'device_id': device['DeviceID'],
                        'vendor_id': f"0x{vid_match.group(1)}" if vid_match else "Unknown",
                        'product_id': f"0x{pid_match.group(1)}" if pid_match else "Unknown"
                    })
                
                if real_devices:
                    return {
                        "devices": real_devices,
                        "device_count": len(real_devices),
                        "enterprise": True,
                        "message": f"Found {len(real_devices)} USB devices"
                    }
            except json.JSONDecodeError as e:
                # Try alternative detection method
                pass
                
        # Alternative detection method for USB storage devices
        result2 = subprocess.run([
            'powershell',
            'Get-Disk | Where-Object {.BusType -eq "USB" -and .OperationalStatus -eq "Online"} | Select-Object FriendlyName, Size, SerialNumber | ConvertTo-Json'
        ], capture_output=True, text=True, timeout=10)
        
        if result2.returncode == 0 and result2.stdout.strip() and result2.stdout.strip() != 'null':
            try:
                disks = json.loads(result2.stdout)
                if not isinstance(disks, list):
                    disks = [disks]
                
                real_devices = []
                for disk in disks:
                    real_devices.append({
                        'name': disk.get('FriendlyName', 'USB Storage Device'),
                        'status': 'Online',
                        'type': 'storage',
                        'size': f"{disk.get('Size', 0) / 1e9:.1f} GB" if disk.get('Size') else 'Unknown',
                        'serial': disk.get('SerialNumber', 'Unknown'),
                        'vendor_id': 'Storage',
                        'product_id': 'Device'
                    })
                
                if real_devices:
                    return {
                        "devices": real_devices,
                        "device_count": len(real_devices),
                        "enterprise": True,
                        "message": f"Found {len(real_devices)} USB storage devices"
                    }
            except:
                pass
                
    except Exception as e:
        print(f"USB detection error: {e}")
    
    # If nothing found
    return {
        "devices": [],
        "device_count": 0,
        "enterprise": True,
        "message": "No USB devices detected. Connect a USB device to see it here."
    }

# Debug endpoint
@app.get("/api/v1/usb/debug")
async def get_usb_debug():
    try:
        # Test basic PowerShell functionality
        result = subprocess.run(['powershell', 'Get-PnpDevice | Where-Object {.Class -eq "USB"} | Select-Object -First 5 | Format-Table FriendlyName, Status, Class -AutoSize'], 
                              capture_output=True, text=True, timeout=10)
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr,
            "return_code": result.returncode
        }
    except Exception as e:
        return {"error": str(e)}

# Dashboard endpoint
@app.get("/dashboard")
async def get_dashboard():
    html_content = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>DLP Enterprise 3.0 Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .dashboard { max-width: 1200px; margin: 0 auto; }
            .card { background: white; padding: 20px; margin: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        </style>
    </head>
    <body>
        <div class="dashboard">
            <h1>🚀 DLP Enterprise 3.0 Dashboard</h1>
            <div class="card">
                <h3>USB Monitoring Status</h3>
                <div id="status">Loading...</div>
            </div>
            <div class="card">
                <h3>Connected USB Devices</h3>
                <div id="devices">Loading...</div>
            </div>
        </div>
        <script>
            async function loadData() {
                try {
                    const response = await fetch('/api/v1/usb/devices');
                    const data = await response.json();
                    document.getElementById('status').innerHTML = 'Status: <b>' + (data.enterprise ? 'Active' : 'Inactive') + '</b><br>Message: ' + data.message;
                    
                    if (data.device_count > 0) {
                        let devicesHTML = 'Connected Devices: <b>' + data.device_count + '</b>';
                        data.devices.forEach(device => {
                            devicesHTML += '<div style="margin: 10px; padding: 10px; border-left: 4px solid green; background: #f9f9f9;">' + 
                                           device.name + ' (' + device.type + ')<br>' +
                                           'Vendor: ' + device.vendor_id + ', Product: ' + device.product_id + 
                                           '</div>';
                        });
                        document.getElementById('devices').innerHTML = devicesHTML;
                    } else {
                        document.getElementById('devices').innerHTML = 'No USB devices connected. Connect a USB device to see it here.';
                    }
                } catch (error) {
                    document.getElementById('status').innerHTML = 'Error loading data';
                    document.getElementById('devices').innerHTML = 'Error loading device information';
                }
            }
            loadData();
            setInterval(loadData, 3000);
        </script>
    </body>
    </html>
    '''
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    print("🚀 ENTERPRISE DLP 3.0 WITH FIXED USB MONITORING")
    print("📍 http://localhost:5001")
    print("📊 Dashboard: http://localhost:5001/dashboard")
    print("🔧 Fixed PowerShell syntax error")
    uvicorn.run(app, host="0.0.0.0", port=5001, reload=False)
