from datetime import datetime
from FlaskWebProject import app, db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from azure.storage.blob import BlobServiceClient
# from azure.storage.blob import BlockBlobService
import string, random
# from werkzeug import secure_filename
from werkzeug.utils import secure_filename
from flask import flash

blob_container = app.config['BLOB_CONTAINER']
blob_service_client = BlobServiceClient.from_connection_string(app.config['BLOB_CONNECTION_STRING'])

def id_generator(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    author = db.Column(db.String(75))
    body = db.Column(db.String(800))
    image_path = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

    def save_changes(self, form, file, user_id, new=False):
        self.title = form.title.data
        self.author = form.author.data
        self.body = form.body.data
        self.user_id = user_id

        if file:
            file_name = secure_filename(file.filename)
            file_extension = file_name.rsplit('.', 1)[1]
            random_file_name = id_generator()
            blob_name = random_file_name + '.' + file_extension
            blob_client = blob_service_client.get_blob_client(container=blob_container, blob=blob_name)

            try:
                # blob_service.create_blob_from_stream(blob_container, file_name, file)
                blob_service_client.create_container(blob_container, 'blob')
                blob_service_client.upload_blob(file.read(), overwrite=True)

                if self.image_path:
                    # blob_service.delete_blob(blob_container, self.image_path)
                    blob_service_client.delete_blobs(self.image_path, file)
            except Exception as e:
                flash(str(e))

            self.image_path = file_name
        if new:
            db.session.add(self)
        db.session.commit()
