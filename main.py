# In your FastAPI app's main.py
import logging
from fastapi import FastAPI, Request

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Outgoing response: Status {response.status_code}")
    return response

@app.get("/")
def root():
    logger.info("Root endpoint called")
    return {"status": "ok"}

@app.get("/health")
def health():
    logger.info("Health check endpoint called")
    return {"status": "healthy"}

@app.get("/debug")
def debug_info():
    """Endpoint to debug network issues"""
    import socket
    import os
    import sys
    import platform
    
    # Get host information
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    # Get environment info
    env_vars = {k: v for k, v in os.environ.items() if not k.startswith('AWS_')}
    
    return {
        "hostname": hostname,
        "local_ip": local_ip,
        "platform": platform.platform(),
        "python_version": sys.version,
        "env_vars": env_vars,
        "network_interfaces": get_network_interfaces()
    }

def get_network_interfaces():
    """Get all network interfaces"""
    import socket
    import fcntl
    import struct
    import array
    
    try:
        # This works on Linux
        max_possible = 128  # arbitrary. raise if needed.
        bytes = max_possible * 32
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        names = array.array('B', b'\0' * bytes)
        outbytes = struct.unpack('iL', fcntl.ioctl(
            s.fileno(),
            0x8912,  # SIOCGIFCONF
            struct.pack('iL', bytes, names.buffer_info()[0])
        ))[0]
        namestr = names.tobytes()
        
        interfaces = {}
        for i in range(0, outbytes, 40):
            name = namestr[i:i+16].split(b'\0', 1)[0].decode()
            ip = socket.inet_ntoa(namestr[i+20:i+24])
            interfaces[name] = ip
        return interfaces
    except Exception as e:
        return {"error": str(e)}