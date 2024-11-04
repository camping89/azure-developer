from datetime import datetime
from FlaskWebProject import app, db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from azure.storage.blob import BlobServiceClient
import string, random
from werkzeug.utils import secure_filename
from flask import flash

blob_container = app.config['BLOB_CONTAINER']
blob_service = BlobServiceClient.from_connection_string(app.config['BLOB_CONNECTION_STRING'])

def id_generator(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    ms_id = db.Column(db.String(200), unique=True)  # Microsoft user ID
    email = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(120))
    is_microsoft_auth = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def generate_random_password():
        # Generate a random string for Microsoft-authenticated users
        return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

    @classmethod
    def create_microsoft_user(cls, ms_id, email, name):
        user = cls(
            username=email,
            ms_id=ms_id,
            email=email,
            name=name,
            is_microsoft_auth=True
        )
        # Set a random password for Microsoft users
        random_password = user.generate_random_password()
        user.set_password(random_password)
        return user


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    subtitle = db.Column(db.String(200))
    author = db.Column(db.String(75))
    body = db.Column(db.String(800))
    image_path = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

    def save_changes(self, form, file, user_id, new=False):
        self.title = form.title.data
        self.subtitle = form.subtitle.data
        self.author = form.author.data
        self.body = form.body.data
        self.user_id = user_id

        if file:
            file_name = secure_filename(file.filename)
            file_extension = file_name.rsplit('.', 1)[1]
            random_file_name = id_generator()
            blob_name = random_file_name + '.' + file_extension
            blob_client = blob_service.get_blob_client(container=blob_container, blob=blob_name)

            try:
                if not blob_service.get_container_client(blob_container).exists():
                    blob_service.create_container(blob_container)
                    
                blob_client.upload_blob(file)
                
                if self.image_path:
                    old_blob_client = blob_service.get_blob_client(container=blob_container, blob=self.image_path)
                    try:
                        if old_blob_client.exists():
                            old_blob_client.delete_blob()
                    except Exception:
                        # Ignore deletion failures
                        pass
                    
            except Exception as e:
                flash(str(e))

            self.image_path = blob_name
        if new:
            db.session.add(self)

        db.session.commit()

    def delete(self):
        try:
            # Delete associated image if it exists
            if self.image_path:
                blob_client = blob_service.get_blob_client(container=blob_container, blob=self.image_path)
                try:
                    if blob_client.exists():
                        blob_client.delete_blob()
                except Exception:
                    # Ignore deletion failures for blob
                    pass
            
            # Delete the post from database
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            flash(str(e))
            return False

    def remove_image(self, should_commit=True):
        try:
            if self.image_path:
                blob_client = blob_service.get_blob_client(container=blob_container, blob=self.image_path)
                try:
                    if blob_client.exists():
                        blob_client.delete_blob()
                except Exception:
                    # Ignore deletion failures
                    pass
                
                self.image_path = None
                if should_commit:
                    db.session.commit()
                return True

        except Exception as e:
            flash(str(e))
            return False
