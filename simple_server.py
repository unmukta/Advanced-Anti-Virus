# SIMPLE USB DETECTION THAT WORKS
from fastapi import FastAPI
import uvicorn
import subprocess
import json

app = FastAPI()

@app.get("/api/v1/usb/devices")
async def get_usb_devices():
    try:
        # Method 1: Get USB devices
        result = subprocess.run([
            'powershell', 
            'Get-PnpDevice | Where-Object {.Class -eq \"USB\" -and .Status -eq \"OK\"} | Select-Object FriendlyName, DeviceID | ConvertTo-Json'
        ], capture_output=True, text=True, timeout=10)
        
        devices = []
        if result.returncode == 0 and result.stdout.strip() and result.stdout.strip() != 'null':
            try:
                devices = json.loads(result.stdout)
                if not isinstance(devices, list):
                    devices = [devices]
            except:
                devices = []
        
        # Method 2: Get USB disks
        result2 = subprocess.run([
            'powershell',
            'Get-Disk | Where-Object {.BusType -eq \"USB\"} | Select-Object FriendlyName, Size | ConvertTo-Json'
        ], capture_output=True, text=True, timeout=10)
        
        disks = []
        if result2.returncode == 0 and result2.stdout.strip() and result2.stdout.strip() != 'null':
            try:
                disks = json.loads(result2.stdout)
                if not isinstance(disks, list):
                    disks = [disks]
            except:
                disks = []
        
        # Combine results
        all_devices = []
        
        for device in devices:
            if 'Hub' not in device['FriendlyName'] and 'Controller' not in device['FriendlyName']:
                all_devices.append({
                    'name': device['FriendlyName'],
                    'type': 'usb_device',
                    'id': device['DeviceID']
                })
        
        for disk in disks:
            all_devices.append({
                'name': disk.get('FriendlyName', 'USB Disk'),
                'type': 'usb_disk',
                'size': f"{int(disk.get('Size', 0)) / (1024*1024*1024):.1f} GB" if disk.get('Size') else 'Unknown'
            })
        
        return {
            "devices": all_devices,
            "count": len(all_devices),
            "message": "Success" if all_devices else "No USB devices found"
        }
        
    except Exception as e:
        return {
            "devices": [],
            "count": 0,
            "message": f"Error: {str(e)}"
        }

if __name__ == "__main__":
    print("🚀 SIMPLE USB DETECTION SERVER")
    uvicorn.run(app, host="0.0.0.0", port=5001)
