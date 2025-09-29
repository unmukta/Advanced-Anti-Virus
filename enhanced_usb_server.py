from fastapi import FastAPI
import uvicorn
import subprocess
import json
import re

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Enhanced USB Monitoring API", "status": "active"}

@app.get("/api/v1/usb/devices")
async def get_usb_devices():
    all_devices = []
    
    # Method 1: USB devices with broader status filter
    try:
        result = subprocess.run([
            'powershell', 
            'Get-PnpDevice | Where-Object {.Class -eq \"USB\" -and (.Status -eq \"OK\" -or .Status -eq \"Unknown\")} | Select-Object FriendlyName, Status, DeviceID | ConvertTo-Json'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and result.stdout.strip() and result.stdout.strip() != 'null':
            try:
                devices = json.loads(result.stdout)
                if not isinstance(devices, list):
                    devices = [devices]
                
                for device in devices:
                    name = device.get('FriendlyName', '')
                    # Skip system USB devices
                    if name and 'Hub' not in name and 'Controller' not in name and 'Host' not in name and 'Root' not in name:
                        # Extract vendor and product IDs
                        vid_match = re.search(r'VID_([0-9A-Fa-f]{4})', device.get('DeviceID', ''), re.IGNORECASE)
                        pid_match = re.search(r'PID_([0-9A-Fa-f]{4})', device.get('DeviceID', ''), re.IGNORECASE)
                        
                        all_devices.append({
                            'name': name,
                            'type': 'usb_device',
                            'status': device.get('Status', 'Unknown'),
                            'vendor_id': f"0x{vid_match.group(1)}" if vid_match else "Unknown",
                            'product_id': f"0x{pid_match.group(1)}" if pid_match else "Unknown",
                            'id': device.get('DeviceID', '')
                        })
            except:
                pass
    except:
        pass
    
    # Method 2: USB disks
    try:
        result2 = subprocess.run([
            'powershell',
            'Get-Disk | Where-Object {.BusType -eq \"USB\"} | Select-Object FriendlyName, Size, OperationalStatus | ConvertTo-Json'
        ], capture_output=True, text=True, timeout=10)
        
        if result2.returncode == 0 and result2.stdout.strip() and result2.stdout.strip() != 'null':
            try:
                disks = json.loads(result2.stdout)
                if not isinstance(disks, list):
                    disks = [disks]
                
                for disk in disks:
                    all_devices.append({
                        'name': disk.get('FriendlyName', 'USB Disk'),
                        'type': 'usb_disk',
                        'status': disk.get('OperationalStatus', 'Unknown'),
                        'size': f"{int(disk.get('Size', 0)) / (1024*1024*1024):.1f} GB" if disk.get('Size') else 'Unknown',
                        'vendor_id': 'Storage',
                        'product_id': 'Device'
                    })
            except:
                pass
    except:
        pass
    
    return {
        "devices": all_devices,
        "count": len(all_devices),
        "message": f"Found {len(all_devices)} USB devices" if all_devices else "No USB devices found"
    }

if __name__ == "__main__":
    print("🚀 ENHANCED USB Monitoring Server Started")
    print("📍 http://localhost:5001")
    print("📋 API: http://localhost:5001/api/v1/usb/devices")
    uvicorn.run(app, host="0.0.0.0", port=5001)
