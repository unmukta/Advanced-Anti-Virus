from fastapi import FastAPI
import uvicorn
import subprocess
import json
import re

app = FastAPI()

def get_unique_usb_devices():
    """Get unique USB devices by filtering duplicates"""
    try:
        # Get all USB devices
        result = subprocess.run([
            'powershell', 
            'Get-PnpDevice -Class USB | Where-Object Status -eq OK | Select-Object FriendlyName, DeviceID, Class, Description | ConvertTo-Json'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and result.stdout.strip() and result.stdout.strip() != 'null':
            try:
                devices = json.loads(result.stdout)
                if not isinstance(devices, list):
                    devices = [devices]
                
                # Remove duplicates and filter system devices
                unique_devices = []
                seen_devices = set()
                
                for device in devices:
                    name = device.get('FriendlyName', '')
                    device_id = device.get('DeviceID', '')
                    
                    # Skip system devices and duplicates
                    if (name and 
                        'Hub' not in name and 
                        'Controller' not in name and 
                        'Host' not in name and
                        'Root' not in name and
                        device_id not in seen_devices):
                        
                        seen_devices.add(device_id)
                        
                        # Extract vendor and product info
                        vid_match = re.search(r'VID_([0-9A-F]{4})', device_id, re.IGNORECASE)
                        pid_match = re.search(r'PID_([0-9A-F]{4})', device_id, re.IGNORECASE)
                        
                        unique_devices.append({
                            'name': name,
                            'device_id': device_id,
                            'vendor_id': f"0x{vid_match.group(1)}" if vid_match else "Unknown",
                            'product_id': f"0x{pid_match.group(1)}" if pid_match else "Unknown",
                            'type': device.get('Class', 'Unknown'),
                            'description': device.get('Description', '')
                        })
                
                return unique_devices
            except Exception as e:
                print(f"JSON error: {e}")
                return []
    except Exception as e:
        print(f"Subprocess error: {e}")
        return []
    
    return []

@app.get("/")
def root():
    return {"message": "Clean USB Monitor - No Duplicates", "status": "active"}

@app.get("/api/v1/usb/devices")
async def get_usb_devices():
    devices = get_unique_usb_devices()
    
    return {
        "devices": devices,
        "count": len(devices),
        "message": f"Found {len(devices)} unique USB devices" if devices else "No USB devices detected"
    }

@app.get("/api/v1/usb/debug")
async def get_debug_info():
    """Debug endpoint to see raw data"""
    try:
        result = subprocess.run([
            'powershell', 
            'Get-PnpDevice -Class USB | Where-Object Status -eq OK | Select-Object FriendlyName, DeviceID, Class | Format-Table -AutoSize'
        ], capture_output=True, text=True, timeout=10)
        
        return {
            "output": result.stdout,
            "error": result.stderr,
            "return_code": result.returncode
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("🚀 CLEAN USB MONITOR - NO DUPLICATES")
    print("📍 http://localhost:5002")
    print("📋 API: http://localhost:5002/api/v1/usb/devices")
    print("🐛 Debug: http://localhost:5002/api/v1/usb/debug")
    uvicorn.run(app, host="0.0.0.0", port=5002)
