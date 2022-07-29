from flask import Flask, render_template
import config
 
app = Flask(__name__)
app.config.from_object(config)
 
 
@app.route('/')
def index():
    return render_template('index.html')
 
 
@app.route('/login_display', methods=['POST', 'GET'])
def sign_in_display():
    return render_template('login.html')
  
 
@app.route('/register_display', methods=['POST', 'GET'])
def sign_up_display():
    return render_template('register.html')
 

if __name__ == '__main__':
    app.run()
