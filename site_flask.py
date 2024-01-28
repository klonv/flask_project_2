import sqlalchemy as sa
import sqlalchemy.orm as so

from app import create_app, db
from app.models import User, Post
# , Message, Notification, Task
from livereload import Server

app = create_app()


# server = Server(app.wsgi_app)
# server.watch
# server.serve(host='127.0.0.1', port=5001)

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa,
            'so': so,
            'db': db,
            'User': User,
            'Post': Post, 
            # 'Message': Message, 
            # 'Notification': Notification, 
            # 'Task': Task,
            }