class RealUSBMonitor:
    def __init__(self):
        self.connected_devices = []
        self.monitoring = False
        
    def start_monitoring(self):
        if self.monitoring:
            return
            
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        print("✅ REAL USB Monitoring: ACTIVATED")
        
    def _monitor_loop(self):
        # Initialize COM for this thread
        pythoncom.CoInitialize()
        
        while self.monitoring:
            try:
                # Use Windows Management Instrumentation to detect real USB devices
                c = wmi.WMI()
                current_devices = []
                
                # Get all USB devices using a different approach
                for item in c.Win32_PnPEntity():
                    if "USB" in str(item.DeviceID):
                        device_info = {
                            'name': item.Name or 'Unknown USB Device',
                            'description': item.Description or '',
                            'status': item.Status or 'Unknown',
                            'type': 'physical',
                            'device_id': item.DeviceID,
                            'vendor_id': self._extract_vendor_id(item.DeviceID),
                            'product_id': self._extract_product_id(item.DeviceID)
                        }
                        current_devices.append(device_info)
                
                self.connected_devices = current_devices
                time.sleep(3)
                
            except Exception as e:
                print(f"USB monitoring error: {e}")
                time.sleep(5)
        
        # Cleanup COM
        pythoncom.CoUninitialize()
    
    def _extract_vendor_id(self, device_id):
        match = re.search(r'VID_([0-9A-Fa-f]{4})', device_id, re.IGNORECASE)
        return f"0x{match.group(1)}" if match else "Unknown"
    
    def _extract_product_id(self, device_id):
        match = re.search(r'PID_([0-9A-Fa-f]{4})', device_id, re.IGNORECASE)
        return f"0x{match.group(1)}" if match else "Unknown"
import subprocess
import json

def get_real_usb_devices():
    \"\"\"Get real USB devices using PowerShell\"\"\"
    try:
        # Use PowerShell to get USB devices
        result = subprocess.run([
            'powershell', 
            'Get-PnpDevice -Class USB | Where-Object {.Status -eq \"OK\"} | Select-Object FriendlyName, Status, DeviceID | ConvertTo-Json'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and result.stdout.strip():
            devices = json.loads(result.stdout)
            if not isinstance(devices, list):
                devices = [devices]
            
            return [{
                'name': device.FriendlyName,
                'status': device.Status,
                'type': 'physical',
                'device_id': device.DeviceID,
                'vendor_id': self._extract_vendor_id(device.DeviceID),
                'product_id': self._extract_product_id(device.DeviceID)
            } for device in devices]
        return []
    except Exception as e:
        print(f"PowerShell USB detection error: {e}")
        return []
