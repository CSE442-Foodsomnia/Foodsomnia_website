from web_app import init_app
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(sys.argv[1])
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000

    print(port)
    app = init_app()
    app.run(debug=True, host='0.0.0.0', port=port)
