# core/monitor.py
import psutil
import time
import json
from collections import deque

class SystemMonitor:
    def __init__(self, smoothing_window=3):
        """
        Initialize system monitor with smoothing for stable readings.
        """
        self.smoothing_window = smoothing_window
        
        # Initialize deques for smoothing values
        self.cpu_readings = deque(maxlen=smoothing_window)
        self.memory_readings = deque(maxlen=smoothing_window)
        self.disk_readings = deque(maxlen=1)
        self.net_sent_readings = deque(maxlen=smoothing_window)
        self.net_recv_readings = deque(maxlen=smoothing_window)
        
        # Network baseline
        self.last_net_io = psutil.net_io_counters()
        self.last_net_time = time.time()
        
        # Initialize with first readings
        self._update_baseline_readings()
        
    def _update_baseline_readings(self):
        """Initialize with baseline readings to avoid spikes on first measurement."""
        # CPU baseline
        self.cpu_readings.append(psutil.cpu_percent(interval=0.1))
        time.sleep(0.1)
        self.cpu_readings.append(psutil.cpu_percent(interval=0.1))
        
        # Memory baseline
        self.memory_readings.append(psutil.virtual_memory().percent)
        
        # Disk baseline
        self.disk_readings.append(psutil.disk_usage('/').percent)
        
        # Network baseline
        net_io = psutil.net_io_counters()
        self.net_sent_readings.append(0)
        self.net_recv_readings.append(0)
        self.last_net_io = net_io
        self.last_net_time = time.time()
    
    def _smooth_value(self, readings, new_value):
        """
        Apply smoothing to a value using a moving average.
        """
        readings.append(new_value)
        return sum(readings) / len(readings)
    
    def get_cpu_usage(self):
        """
        Get smoothed CPU usage percentage.
        """
        cpu_percent = psutil.cpu_percent(interval=0.5)
        return self._smooth_value(self.cpu_readings, cpu_percent)
    
    def get_memory_usage(self):
        """
        Get smoothed memory usage percentage.
        """
        memory_percent = psutil.virtual_memory().percent
        return self._smooth_value(self.memory_readings, memory_percent)
    
    def get_disk_usage(self):
        """
        Get disk usage percentage for the root partition.
        """
        disk_percent = psutil.disk_usage('/').percent
        self.disk_readings.append(disk_percent)
        return disk_percent
    
    def get_network_usage(self):
        """
        Calculate network usage in MB/s.
        """
        current_time = time.time()
        current_net_io = psutil.net_io_counters()
        
        # Calculate time difference
        time_diff = current_time - self.last_net_time
        if time_diff < 0.5:
            if self.net_sent_readings and self.net_recv_readings:
                return (
                    sum(self.net_sent_readings) / len(self.net_sent_readings),
                    sum(self.net_recv_readings) / len(self.net_recv_readings)
                )
            return (0, 0)
        
        # Calculate bytes per second
        sent_speed = (current_net_io.bytes_sent - self.last_net_io.bytes_sent) / time_diff
        recv_speed = (current_net_io.bytes_recv - self.last_net_io.bytes_recv) / time_diff
        
        # Convert to MB/s
        sent_speed_mb = sent_speed / (1024 * 1024)
        recv_speed_mb = recv_speed / (1024 * 1024)
        
        # Update stored values
        self.last_net_io = current_net_io
        self.last_net_time = current_time
        
        # Apply smoothing
        smoothed_sent = self._smooth_value(self.net_sent_readings, sent_speed_mb)
        smoothed_recv = self._smooth_value(self.net_recv_readings, recv_speed_mb)
        
        return (smoothed_sent, smoothed_recv)
    
    def get_top_processes(self, count=5):
        """
        Get top processes by CPU and memory usage.
        """
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_percent', 'cpu_percent']):
            try:
                proc_info = proc.info
                proc_info['memory_percent'] = proc_info['memory_percent'] or 0
                proc_info['cpu_percent'] = proc_info['cpu_percent'] or 0
                processes.append(proc_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        # Sort by CPU usage (descending) and get top ones
        processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
        return processes[:count]
    
    def get_all_metrics(self):
        """
        Get all system metrics in a single call.
        """
        cpu_usage = self.get_cpu_usage()
        memory_usage = self.get_memory_usage()
        disk_usage = self.get_disk_usage()
        net_sent, net_recv = self.get_network_usage()
        top_processes = self.get_top_processes()
        
        return {
            'cpu_usage': round(cpu_usage, 1),
            'memory_usage': round(memory_usage, 1),
            'disk_usage': round(disk_usage, 1),
            'network_sent_mb': round(net_sent, 3),
            'network_recv_mb': round(net_recv, 3),
            'top_processes': top_processes,
            'timestamp': time.time()
        }

def get_system_metrics():
    """
    Get current system metrics as a one-time call.
    Useful for PowerShell integration.
    """
    monitor = SystemMonitor()
    return monitor.get_all_metrics()

if __name__ == "__main__":
    # If run directly, output JSON
    metrics = get_system_metrics()
    print(json.dumps(metrics, indent=2))
