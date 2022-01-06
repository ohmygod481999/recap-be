from app import app
import os

port = os.environ.get("PORT", 5001)

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=port)
