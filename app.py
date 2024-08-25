from flask import Flask,render_template,request
import sqlite3,pickle
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contact',methods=['GET','POST'])
def contactus():
    if request.method=='POST':
        Fullname = request.form.get('name')
        Phone = request.form.get('phone')
        Email = request.form.get('email')
        Address = request.form.get('address')
        Message = request.form.get('message')
        conn = sqlite3.connect('ytdatabase.db')
        cur = conn.cursor()
        cur.execute(f'''
                insert into contact values("{Fullname}","{Phone}","{Email}","{Address}","{Message}")
        ''')
        conn.commit()
        return render_template('message.html')
        
    else:
        return render_template('contactus.html')

@app.route('/analytical')
def analytical():
    return render_template('analytical.html')

@app.route('/predict',methods=['GET','POST'])
def predict():
    if request.method=='POST':
       
        views = request.form['views']
        dislikes = request.form['dislikes']
        comment_count = request.form['comment_count']
    
        genre = request.form['genre']
        #print(category_id,views,dislikes,comment_count,ratings_disabled,video_error_or_removed,genre)


        with open('model.pickle','rb') as mod:
            model=pickle.load(mod)
        pred = model.predict([[float(views),float(dislikes),float(comment_count),float(genre)]])
        return render_template('result.html',pred = str(round(pred[0])))
    else:
        return render_template('likepredict.html')









if __name__ == '__main__':
    app.run(host = '0.0.0.0',port = 5050)