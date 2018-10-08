from app import app, db
from app.models import User, Post

# app.run(debug=True, port=9999)
app.run(port=9999)



@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
