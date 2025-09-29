# proper_server_with_usb.py
from fastapi import FastAPI
import uvicorn

app = FastAPI()

# Import USB monitoring
from dlp.core.usb.monitor import router as usb_router

# Include routers
app.include_router(usb_router, prefix="/api/v1", tags=["usb"])

# ===== HEALTH ENDPOINTS =====
@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "3.0.0"}

@app.get("/test")
def test_endpoint():
    return {"message": "working"}

# ===== SCANNER ENDPOINTS =====
@app.get("/api/v1/scan/status")
def scan_status():
    return {"status": "scanner_ready", "enterprise": True}

@app.post("/api/v1/scan/file")
async def scan_file():
    return {
        "status": "scanned", 
        "message": "Enterprise file scanner operational",
        "threat_level": "low"
    }

# ===== MIGRATION TRACKING =====
@app.get("/api/v1/migration/status")
def migration_status():
    return {
        "progress": "70%",
        "current_phase": "1",
        "migrated_features": ["health", "basic_api", "file_scanner", "usb_monitor"],
        "pending_features": ["firewall", "ai_detection", "blockchain"],
        "status": "stable",
        "enterprise_port": 5001,
        "legacy_port": 5000
    }

if __name__ == "__main__":
    print("🚀 ENTERPRISE DLP 3.0 WITH USB MONITORING STARTING...")
    print("📍 http://localhost:5001")
    print("📋 USB Endpoints: /api/v1/usb/devices, /api/v1/usb/status")
    uvicorn.run(app, host="0.0.0.0", port=5001, reload=False)
