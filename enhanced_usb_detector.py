from fastapi import FastAPI
import uvicorn
import subprocess
import json
from datetime import datetime

app = FastAPI()

def get_usb_storage():
    """Multiple methods to detect USB storage"""
    try:
        # Method 1: Check for removable drives (most reliable)
        result = subprocess.run([
            'powershell', 
            'Get-Volume | Where-Object {.DriveType -eq \"Removable\" -and .DriveLetter} | Select-Object DriveLetter, FileSystemLabel, Size, SizeRemaining | ConvertTo-Json'
        ], capture_output=True, text=True, timeout=10)
        
        devices = []
        current_time = datetime.now().strftime("%H:%M:%S")
        
        if result.returncode == 0 and result.stdout.strip() and result.stdout.strip() != 'null':
            try:
                volumes = json.loads(result.stdout)
                if not isinstance(volumes, list):
                    volumes = [volumes]
                
                for volume in volumes:
                    if volume.get('DriveLetter'):
                        devices.append({
                            'name': f"Drive {volume.get('DriveLetter')}: {volume.get('FileSystemLabel', 'Removable Disk')}",
                            'type': 'usb_volume',
                            'size': f"{int(volume.get('Size', 0)) / (1024**3):.1f} GB" if volume.get('Size') else 'Unknown',
                            'free_space': f"{int(volume.get('SizeRemaining', 0)) / (1024**3):.1f} GB" if volume.get('SizeRemaining') else 'Unknown',
                            'status': 'Connected',
                            'detected_at': current_time,
                            'detection_method': 'volume_detection'
                        })
            except:
                pass
        
        # If no volumes found, try disk method
        if not devices:
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
                        if disk.get('OperationalStatus') == 'Online':
                            devices.append({
                                'name': disk.get('FriendlyName', 'USB Storage Device'),
                                'type': 'usb_disk',
                                'size': f"{int(disk.get('Size', 0)) / (1024**3):.1f} GB" if disk.get('Size') else 'Unknown',
                                'status': disk.get('OperationalStatus', 'Unknown'),
                                'detected_at': current_time,
                                'detection_method': 'disk_detection'
                            })
                except:
                    pass
                
        return devices
        
    except Exception as e:
        print(f"Detection error: {e}")
        return []

@app.get("/")
def root():
    return {"message": "Enhanced USB Detector", "status": "active"}

@app.get("/api/v1/usb/devices")
async def get_usb_devices():
    devices = get_usb_storage()
    
    return {
        "devices": devices,
        "count": len(devices),
        "message": f"Found {len(devices)} USB devices" if devices else "No USB devices detected. Connect a USB drive.",
        "last_scan": datetime.now().strftime("%H:%M:%S")
    }

@app.get("/api/v1/usb/debug")
async def get_debug_info():
    """Debug endpoint to see what Windows detects"""
    try:
        # Check what volumes Windows sees
        result = subprocess.run([
            'powershell', 
            'Get-Volume | Format-Table DriveLetter, FileSystemLabel, Size, DriveType -AutoSize'
        ], capture_output=True, text=True, timeout=10)
        
        return {
            "volume_info": result.stdout,
            "error": result.stderr,
            "return_code": result.returncode
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("🚀 ENHANCED USB DETECTOR")
    print("📍 http://localhost:5001")
    print("📋 API: http://localhost:5001/api/v1/usb/devices")
    print("🐛 Debug: http://localhost:5001/api/v1/usb/debug")
    uvicorn.run(app, host="0.0.0.0", port=5001)
