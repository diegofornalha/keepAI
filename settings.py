import os


class Settings:
    def __init__(self):
        self.FLASK_ENV = os.getenv("FLASK_ENV", "development")
        self.DEBUG = self.FLASK_ENV == "development"
        self.TESTING = False
        self.SECRET_KEY = os.getenv("SECRET_KEY", "dev-key-change-this-in-production")

        # Configurações do Supabase
        self.SUPABASE_URL = os.getenv("SUPABASE_URL")
        self.SUPABASE_KEY = os.getenv("SUPABASE_KEY")

        # Configurações do Flask
        self.TEMPLATES_AUTO_RELOAD = True
        self.SEND_FILE_MAX_AGE_DEFAULT = 0 if self.DEBUG else 31536000
