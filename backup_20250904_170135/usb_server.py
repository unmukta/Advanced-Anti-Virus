from fastapi import FastAPI
import uvicorn
import subprocess
import json

app = FastAPI()

@app.get("/")
def root():
    return {"message": "USB Monitoring API", "status": "active"}

@app.get("/api/v1/usb/devices")
async def get_usb_devices():
    try:
        # CORRECT PowerShell syntax with .Class and .Status
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
        
        # Filter out system USB devices
        real_devices = []
        for device in devices:
            name = device.get('FriendlyName', '')
            if name and 'Hub' not in name and 'Controller' not in name and 'Host' not in name:
                real_devices.append({
                    'name': name,
                    'type': 'usb_device',
                    'id': device.get('DeviceID', '')
                })
        
        return {
            "devices": real_devices,
            "count": len(real_devices),
            "message": f"Found {len(real_devices)} USB devices" if real_devices else "No USB devices found"
        }
        
    except Exception as e:
        return {
            "devices": [],
            "count": 0,
            "message": f"Error: {str(e)}"
        }

if __name__ == "__main__":
    print("🚀 USB Monitoring Server Started")
    print("📍 http://localhost:5001")
    print("📋 API: http://localhost:5001/api/v1/usb/devices")
    uvicorn.run(app, host="0.0.0.0", port=5001)
