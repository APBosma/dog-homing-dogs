from app import app

print("in web")
print("running app")

if __name__ == "__main__":
    print("at the bottom of web.py")
    app.run(debug=True)
