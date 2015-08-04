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

def ExcludeIngredient(d, bad_ing):
    if not isinstance(bad_ing,list):
        bad_ing = [bad_ing]
    bools = []
    for i, inglist in enumerate(d.ingredients):
        bools.append(True)
        for ing in inglist:
            for bad in bad_ing:
                if bad.lower() in ing.lower():
                    bools[i]=False
                    break
    return d[bools]

def SortBy(d, choice):
    if choice == 'pricelow':
        return d.sort(['price'], ascending=[1])
    elif choice == 'pricehigh':
        return d.sort(['price'], ascending=[0])
    elif choice == 'ratinglow':
        return d.sort(['rating'], ascending=[1])
    elif choice == 'ratinghigh':
        return d.sort(['rating'], ascending=[0])
    else:
        return d

app = Flask(__name__)

with open('AllProducts071715.txt', 'rb') as f:
    dsl = f.read().splitlines()
data_json_str = "[" + ','.join(dsl) + "]"
df = pd.read_json(data_json_str)
df = df[['name','categories','ingredients','pros','cons','rating','nreviews','price']]
df_show = df.copy()
#cats = set([item for sublist in df.categories[:10] for item in sublist])

@app.route('/')
def hello():
   return render_template("index.html", data=df_show.to_html())

@app.route('/select', methods = ['POST'])
def select():
    global df_show
    
    #pick a category
    cat = request.form['category']
    cat = str(cat)
    if cat != "":
        df_show = PickCategories(df_show, cat)
    
    #exclude an ingredient
    ingr = request.form['ingredient']
    ingr = str(ingr)
    if ingr != "":
        df_show = ExcludeIngredient(df_show,ingr)
    
    #sort by
    sortby = request.form['sort']
    df_show = SortBy(df_show,sortby)
    
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
