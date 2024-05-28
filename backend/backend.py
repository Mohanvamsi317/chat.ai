from flask import Flask,request,jsonify 
from pymongo import MongoClient
import openai 
import os

openai.api_key=os.getenv("OPENAI_API_KEY")
openai_mode='api'


def generate_response(prompt):
    response=openai.Completion.create(engine="text-davinci-003",
                                      prompt=prompt,
                                      max_tokens=1024,
                                      n=1,
                                      temperature=0.7)
    return response["choices"][0]["text"] 




#def generate_response(prompt):
#    openai.api_key=openaikey
#    openai.default_headers = {"x-foo": "true"}
#    chat_completion = openai.chat.completions.create(
#    messages=[
#        {
#            "role": "user",
#            "content": "Say this is a test",
#        }
#    ],
#    model="gpt-3.5-turbo",
#		)
#    return chat_completion

client=MongoClient('127.0.0.1',27017)
db=client['chat'] 
collection=db['ai'] 

api=Flask(__name__)

@api.route('/register', methods=['post', 'get'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        emailid = request.form.get('emailid')
        mobile = request.form.get('mobile')
        password = request.form.get('password')
        k = {}
        k['name'] = name
        k['emailid'] = emailid
        k['mobile'] = mobile
        k['password'] = password
        print("enter")
        query = {'$or': [{'emailid': emailid}, {'mobile': mobile}]}

        # Check if account already exists
        if collection.find_one(query):
            print("account exists")
            return 'account exists'
        
        # If account doesn't exist, insert the new data
        collection.insert_one(k)
        return 'data stored'

   

@api.route('/login',methods=['get'])
def login():
    emailid=request.args.get('emailid')
    password=request.args.get('password')
    query={'emailid':emailid}
    for i in collection.find(query):
         if(i['password']==password):
            return 'True'
    return 'False'

@api.route('/chat', methods=['get','post'])
def chat():
    user_message = request.form.get('message') 
    print(user_message) 
    bot_response = generate_response(user_message)
    collection.insert_one({'message':user_message,'type':'user'})
    collection.insert_one({'message': bot_response, 'type': 'bot'})

    response = {'message': bot_response}
    
    return jsonify(response)

#    user_message = request.args.get('message')  
#    bot_response = generate_response(user_message)
#    return jsonify({"message": bot_response['choices'][0]['message']['content']})
#    if request.method == 'GET':
#        user_message = request.args.get('message')
#    elif request.method == 'POST':
#        user_message = request.form.get('message')
#    else:
#        return jsonify({"error": "Invalid request method"})

#    bot_response = generate_response(user_message)
#   return jsonify({"message": bot_response['choices'][0]['message']['content']})

 

if __name__=="__main__":
    api.run(host='0.0.0.0',port=5001,debug=True)
