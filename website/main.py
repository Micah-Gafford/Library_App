from library import create_app
import config

# Setup
app = create_app()

if __name__ == "__main__":
  app.run(debug=True)