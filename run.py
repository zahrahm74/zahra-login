#!/usr/bin/env python3
"""
Flask Application Startup Script
Simple script to run the Flask application with proper configuration.
"""

import os
import sys
from app import app, db

def main():
    """Main startup function"""
    print("🚀 Starting Flask Application...")
    print("=" * 50)
    
    # Check if we're in development mode
    if os.getenv('FLASK_ENV') == 'development':
        print("📝 Development mode enabled")
        print("🔧 Debug mode: ON")
        print("🌐 Server will be accessible at: http://localhost:5000")
        print("📊 API documentation: http://localhost:5000/api")
        print("=" * 50)
    
    try:
        # Create database tables
        with app.app_context():
            db.create_all()
            print("✅ Database initialized successfully")
        
        # Run the application
        app.run(
            host='0.0.0.0',
            port=int(os.getenv('PORT', 5000)),
            debug=os.getenv('FLASK_ENV') == 'development'
        )
        
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()