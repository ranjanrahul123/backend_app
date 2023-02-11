from flask import Flask,render_template,request,redirect,url_for,session,flash,Response
from datetime import datetime,timedelta
from translate import Translate
from summarize import Summarize

app = Flask(__name__)
app.secret_key = "asdkjfbaskdljfouaksdhfklsadhlfhsdlifhsk"
app.permanent_session_lifetime = timedelta(days=5)

@app.route("/",methods = ["GET"])
def home():
    return "HOME"
@app.route("/translate",methods = ["GET","POST"])
def translate():
    json_data  = request.json 
    text       = json_data["text"]
    target_lan = json_data["target"].lower()
    print(text,target_lan)
    
    # text ="I would really like to drive your car around the block a few times"
    # target_lan ='fr'
    
    translate_object = Translate()
    # print(translate_object)
    return Response(translate_object.translate(text,target_lan), mimetype="application/json")

@app.route("/summarize", methods = ["POST"])
def summarize():
    json_data = request.json 
    text      = json_data["text"]
    #text ="I would really like to drive your car around the block a few times"
    summarize_object = Summarize()
    result = summarize_object.get_summary(text)
    print(result)
    return Response(result, mimetype="application/json")

if __name__ == "__main__":
    app.run(debug = True)
