from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import request,redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo.db'
app.config['SQLALCHEMY_DATABASE_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Todo(db.Model):
    Sno= db.Column(db.Integer,primary_key=True)
    Title=db.Column(db.String(200),nullable=False)
    Desc=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self)->str:
        return f"{self.Sno}-{self.Title}"

@app.route("/",methods=['GET','POST'])
def hello_world():
    if request.method=="POST":
        title=request.form.get("title")
        desc=request.form.get("desc")
        print("Received Data:", title, desc)
        ntodo=Todo(Title=title,Desc=desc)
        db.session.add(ntodo)
        db.session.commit()
        print("Todo added successfully!")
    
    alltodo=Todo.query.all()
    print(alltodo)
    return render_template('index.html',alltodo=alltodo)

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title=request.form.get("title")
        desc=request.form.get("desc")
        todo=Todo.query.filter_by(Sno=sno).first()
        todo.Title=title
        todo.Desc=desc
        db.session.commit()
        return redirect('/')
    todo=Todo.query.filter_by(Sno=sno).first()
    return render_template('update.html',todo=todo)


@app.route('/delete/<int:sno>')
def delete(sno):
    todo=Todo.query.filter_by(Sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__=="__main__":
      with app.app_context():
           db.create_all()
      app.run(debug=True,port=8000)