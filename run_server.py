"""
Start FastAPI Backend Server
Script untuk menjalankan FastAPI backend dengan error handling
"""

import subprocess
import sys
import time
from pathlib import Path

def run_fastapi_server():
    """Run FastAPI server dengan Uvicorn"""
    
    print("=" * 70)
    print("🚀 FastAPI Backend Server")
    print("=" * 70)
    
    # Check jika database sudah ada
    db_path = Path("soft_ai_pro.db")
    if not db_path.exists():
        print("\n⚠️  Database tidak ditemukan!")
        print("   Membuat database baru...")
        try:
            exec(open("setup_database.py").read())
        except Exception as e:
            print(f"   ❌ Error: {e}")
            print("   Jalankan: python setup_database.py")
            return False
    
    print("\n✅ Database OK: soft_ai_pro.db")
    
    # Start Uvicorn server
    print("\n📡 Starting Uvicorn server...")
    print("   Host: 127.0.0.1")
    print("   Port: 8000")
    print("   Docs: http://127.0.0.1:8000/docs")
    print("\n" + "=" * 70)
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "app:app",
            "--host", "127.0.0.1",
            "--port", "8000",
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n\n⏹️  Server stopped")
        return True
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


if __name__ == "__main__":
    success = run_fastapi_server()
    sys.exit(0 if success else 1)
