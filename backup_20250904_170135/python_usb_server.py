from fastapi import FastAPI
import uvicorn
import pyudev

app = FastAPI()

def get_usb_devices():
    """Detect USB devices using pyudev (no PowerShell needed)"""
    context = pyudev.Context()
    devices = []
    
    # Get all USB devices
    for device in context.list_devices(subsystem='usb'):
        if device.device_type == 'usb_device':
            vendor_id = device.get('ID_VENDOR_ID', 'Unknown')
            product_id = device.get('ID_MODEL_ID', 'Unknown')
            vendor_name = device.get('ID_VENDOR_FROM_DATABASE', device.get('ID_VENDOR', 'Unknown'))
            product_name = device.get('ID_MODEL_FROM_DATABASE', device.get('ID_MODEL', 'Unknown'))
            
            # Skip USB hubs and controllers
            if 'hub' not in product_name.lower() and 'root' not in product_name.lower():
                devices.append({
                    'name': f"{vendor_name} {product_name}",
                    'vendor_id': vendor_id,
                    'product_id': product_id,
                    'type': 'usb_device',
                    'sys_path': device.sys_path
                })
    
    # Also check block devices (USB storage)
    for device in context.list_devices(subsystem='block'):
        if device.get('ID_BUS') == 'usb':
            devices.append({
                'name': device.get('ID_MODEL', 'USB Storage Device'),
                'vendor_id': device.get('ID_VENDOR_ID', 'Unknown'),
                'product_id': device.get('ID_MODEL_ID', 'Unknown'),
                'type': 'usb_storage',
                'size': device.get('ID_PART_TABLE_TYPE', 'Unknown'),
                'sys_path': device.sys_path
            })
    
    return devices

@app.get("/")
def root():
    return {"message": "Python-Only USB Monitoring API", "status": "active"}

@app.get("/api/v1/usb/devices")
async def get_usb_devices():
    try:
        devices = get_usb_devices()
        return {
            "devices": devices,
            "count": len(devices),
            "message": f"Found {len(devices)} USB devices" if devices else "No USB devices found"
        }
    except Exception as e:
        return {
            "devices": [],
            "count": 0,
            "message": f"Error: {str(e)}"
        }

if __name__ == "__main__":
    print("🚀 PYTHON-ONLY USB Monitoring Server Started")
    print("📍 http://localhost:5001")
    print("📋 API: http://localhost:5001/api/v1/usb/devices")
    uvicorn.run(app, host="0.0.0.0", port=5001)
