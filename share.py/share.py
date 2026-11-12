from pyngrok import ngrok

# Open a tunnel on port 5000 (where your Flask app runs)
public_url = ngrok.connect(5000)
print(" * Public URL:", public_url)