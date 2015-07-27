from flask import Flask, render_template, request, redirect
import pandas as pd

def PickCategories(d, mycats):
    if not isinstance(mycats, list):
        mycats = [mycats]
    bools = []
    for catlist in d.categories:
        if len(list(set(catlist)&set(mycats))) == 0:
            bools.append(False)
        else:
            bools.append(True)
    return d[bools]

def Tester(s):
    print s

app = Flask(__name__)

with open('AllProducts071715.txt', 'rb') as f:
    dsl = f.read().splitlines()
data_json_str = "[" + ','.join(dsl) + "]"
df = pd.read_json(data_json_str)
df_show = df.copy()
#cats = set([item for sublist in df.categories[:10] for item in sublist])

@app.route('/')
def hello():
   return render_template("index.html", data=df_show.to_html())

@app.route('/select', methods = ['POST'])
def select():
    global df_show
    cat = request.form['category']
    cat = str(cat)
    df_show = PickCategories(df_show, cat)
    return redirect('/')

@app.route('/reset', methods = ['POST'])
def reset():
    global df_show
    global df
    df_show = df.copy()
    return redirect('/')
	
if __name__ == '__main__':
    app.run()



# printing df
#   {% block content %}
#   {{data | safe}}
#   {% endblock %}



#   {% block content %}
#   {{data | safe}}
#   {% endblock %}
