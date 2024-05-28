from flask import Flask,render_template,redirect,request,session
import urllib3
import json

backendServer='http://127.0.0.1:5001'
registerapi='/register'
loginapi='/login'
chatapi='/chat'

frontend=Flask(__name__)
frontend.secret_key='litam'

@frontend.route('/')
def homePage():
    return render_template('register.html')

@frontend.route('/register')
def registerPage():
    return render_template('register.html')
@frontend.route('/login')
def loginPage():
    return render_template('login.html')

@frontend.route('/dashboard')
def dashboardPage():
    return render_template('chatbot.html')

@frontend.route('/register', methods=['POST', 'GET'])
def registerForm():
    if request.method=='POST':
        name = request.form['name']
        mobile = request.form['mobile']
        password = request.form['password']
        emailid = request.form['emailid']
        print(name, mobile, password, emailid)

        # Use the correct route here
        api = backendServer + registerapi
        http = urllib3.PoolManager()
        response = http.request('post', api, fields={'name': name, 'mobile': mobile, 'password': password, 'emailid': emailid})

        response = response.data.decode('utf-8')

        if response == 'account exists':
            return render_template('register.html', err=response)
        else:
            return render_template('register.html', res='Account Created Successfully')
    else:
        # Handle the GET request separately, if needed
        # For example, render a registration form
        return render_template('register.html')
  

@frontend.route('/loginForm', methods=['GET', 'POST'])
def loginForm():
    if request.method == 'POST':
        emailid = request.form['emailid']
        password = request.form['password']
        print(emailid, password)
        api = backendServer + loginapi + '?' + 'emailid=' + emailid + '&password=' + password
        http = urllib3.PoolManager()
        response = http.request('get', api)
        response = response.data
        response = response.decode('utf-8')
        if response == 'True':
            session['emailid'] = emailid
            return redirect('/dashboard')
        else:
            return render_template('login.html', err='Invalid Login')
    else:
        # Handle the GET request separately, if needed
        # For example, render a login form
        return render_template('login.html')


@frontend.route('/chat', methods=['get', 'post'])
def chat():
    if request.method == 'POST':
        message = request.form.get('message')
        print("Frontend Message:", message)  # Add this line for debugging
        api = backendServer + chatapi
        http = urllib3.PoolManager()

        try:
            response = http.request('post', api, fields={'message': message})
            response = response.data
            response = response.decode('utf-8')
            print("Backend Response:", response)  # Add this line for debugging
            response_json = json.loads(response)
            answer = response_json['message']
            return render_template('chatbot.html', res=answer)

        except json.decoder.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return render_template('chatbot.html', err="Invalid JSON response from backend")

    # If it's a GET request, handle it appropriately
    return render_template('chatbot.html', res='')  # Provide any default value if needed






if __name__=="__main__":
    frontend.run('0.0.0.0',port=5000,debug=True)