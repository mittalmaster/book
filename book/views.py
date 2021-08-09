from django.shortcuts import render
#by me
from django.http import HttpResponse

import joblib
import numpy as np
import pandas as pd
import csv
# Create your views here.


#read csv file
data = []
with open("bookdata.csv") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        data.append(row)







#Trained Model
model = joblib.load("final_model.sav")

book_pivot = joblib.load("bp.sav")

ans = []

def recommend_book(book_name):
    book_id = np.where(book_pivot.index == book_name)[0]
    print(book_id)
    ans = []
    if(book_id.size == 0):
        return ans
    distances, suggestions = model.kneighbors(book_pivot.iloc[book_id, :].values.reshape(1, -1), n_neighbors=6)
    for i in range(len(suggestions)):
        if not i:
            ans.append(book_pivot.index[suggestions[i]])
        else:
            ans.append(0)
    print(ans)
    return ans



bookdata = pd.read_csv('bookdata.csv')

def index(request):
    book = pd.read_csv('top100.csv')

    uid = book['ISBN'].tolist()
    imgm = book['imgm'].tolist()
    name = book['title'].tolist()
    mylist = zip(imgm, name,uid)
    context = {
        'mylist': mylist,
    }

    return render(request, 'home.html', context)



def NotFound(request):
    return render(request,'NotFound.html')



def resultclick(request,id):
    val = id
    col = [x[1] for x in data]


    while(len(val)!=10):
        val = '0' + val

    for i in range(0,len(data)):
        if val == col[i]:
            #print(i)
            break
    book_info = data[i]
    #print(book_info)


    answer= []
    if len(book_info)!=0:
        #print(book_info[2])
        answer = recommend_book(book_info[2])




    if len(answer) == 0:
        answer = book_info[2]
        boolean_series = bookdata.title.isin(answer)

    else:
        boolean_series = bookdata.title.isin(answer[0])

    #print(answer)
    #boolean_series = bookdata.title.isin(answer[0])
    filtered_df = bookdata[boolean_series]



    actual = filtered_df

    #print(actual)
    if actual.shape == 0:
        return render(request, 'NotFound.html')

    uid = actual['ISBN'].tolist()
    imgm = actual['imgm'].tolist()
    name = actual['title'].tolist()
    mylist = zip(imgm, name, uid)
    context = {
        'mylist': mylist,
    }

    return render(request, 'resultclick.html',{'mylist':mylist})



def result(request):
    val = request.GET['book']

    answer = recommend_book(val)
    print(answer)
    if len(answer)==0:
        answer = [val]
        print(answer)

    else:
        answer = answer[0].tolist()
    boolean_series = bookdata.title.isin(answer)
    actual = bookdata[boolean_series]
    actual.drop_duplicates(['title'], inplace=True)
    if len(actual)==0:
        return render(request,'NotFound.html')

    uid = actual['ISBN'].tolist()
    imgm = actual['imgm'].tolist()
    name = actual['title'].tolist()
    mylist = zip(imgm, name, uid)
    context = {
        'mylist': mylist,
    }
    return render(request,'result.html',{'mylist':mylist})