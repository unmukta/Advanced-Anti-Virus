from fastapi import FastAPI
import uvicorn
import subprocess
import json
from datetime import datetime

app = FastAPI()

def get_physical_usb_storage():
    """Detect only physical USB storage devices"""
    try:
        # Get physical USB disks
        result = subprocess.run([
            'powershell', 
            'Get-Disk | Where-Object BusType -eq USB | Where-Object OperationalStatus -eq Online | Select-Object FriendlyName, Size, SerialNumber | ConvertTo-Json'
        ], capture_output=True, text=True, timeout=10)
        
        devices = []
        current_time = datetime.now().strftime("%H:%M:%S")
        
        if result.returncode == 0 and result.stdout.strip() and result.stdout.strip() != 'null':
            try:
                disks = json.loads(result.stdout)
                if not isinstance(disks, list):
                    disks = [disks]
                
                for disk in disks:
                    # Only include physical USB storage devices
                    if disk.get('Size') and int(disk.get('Size', 0)) > 0:
                        devices.append({
                            'name': disk.get('FriendlyName', 'USB Storage Device'),
                            'size': f"{int(disk.get('Size', 0)) / (1024**3):.1f} GB",
                            'serial': disk.get('SerialNumber', 'Unknown'),
                            'status': 'Connected',
                            'detected_at': current_time
                        })
            except:
                pass
                
        return devices
        
    except Exception as e:
        print(f"Error: {e}")
        return []

@app.get("/")
def root():
    return {"message": "DLP USB Storage Monitor", "status": "active"}

@app.get("/api/v1/usb/devices")
async def get_usb_devices():
    devices = get_physical_usb_storage()
    
    return {
        "devices": devices,
        "count": len(devices),
        "message": f"Found {len(devices)} physical USB storage devices" if devices else "No physical USB storage devices connected",
        "last_scan": datetime.now().strftime("%H:%M:%S")
    }

if __name__ == "__main__":
    print("🚀 DLP USB STORAGE MONITOR")
    print("📍 http://localhost:5001")
    print("📋 API: http://localhost:5001/api/v1/usb/devices")
    print("💡 Only detects physical USB storage devices")
    uvicorn.run(app, host="0.0.0.0", port=5001)
