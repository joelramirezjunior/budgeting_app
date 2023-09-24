from app.app import app
import config

app.config.from_object(config.DevelopmentConfig)

if __name__ == '__main__':
    app.run()
