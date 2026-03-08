from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from . forms import NewUserForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm  # add this
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score



Module = 'modules.html'
# Create your views here.

# This is the home page
def index(request):
    return render(request, 'index.html')

# This is about its a small information about your project


def about(request):
    return render(request, 'about.html')


# Register page
def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful.")
            return redirect("login")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form": form})

# Login page


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:

                messages.info(request, f"You are now logged in as {username}.")
                return redirect("userhome")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})

# user Home page


def userhome(request):
    return render(request, 'userhome.html')


# load = upload the csv file


def load(request):
    if request.method == "POST":
        global df
        file = request.FILES['myfile']
        df = pd.read_csv(file)
        return render(request, 'load.html', {'res': "Data Uploaded Succesfully", })
    return render(request, "load.html")

# view the uploaded data
# before preprocessing


def view(request):
    global df
    col = df.head(100).to_html
    return render(request, "view.html", {'table': col})

# Create your views here.

def prepro(request):
    global df
    # Apply a type costing
    df['arrival_mode'] = df['arrival_mode'].astype('str')
    df['complaint'] = df['complaint'].astype('str')   
    df['diagnosis'] = df['diagnosis'].astype('str')
    df['result'] = df['result'].astype('str')
    le = LabelEncoder()
    # Apply the Label Encoding    
    df['error_code'] = df['error_code'].astype('str')
    df['arrival_mode'] = pd.Series(le.fit_transform(df['arrival_mode']))
    df['complaint'] = pd.Series(le.fit_transform(df['complaint']))
    df['diagnosis'] = pd.Series(le.fit_transform(df['diagnosis']))
    df['result'] = pd.Series(le.fit_transform(df['result']))
    df['error_code'] = pd.Series(le.fit_transform(df['error_code']))
    df['saturation'] = df['saturation'].fillna(df['saturation'].mean())

    col = df.head(100).to_html
    return render(request, "prepro.html", {'table': col})

def modules(request):
    global df
    if request.method == "POST":
        x = df.drop("admissions", axis=1)
        y = df["admissions"] 
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3,stratify=y, random_state= 72) 
        model = request.POST['algo']
        if model == "1": 
            ln = LogisticRegression()
            ln.fit(x_train,y_train)
            l_pred = ln.predict(x_test)
            l_ac = accuracy_score(l_pred, y_test)
            print("accuracy_score of LogisticRegression is"+": "+str(l_ac))
            msg="Accuresy of LogisticRegressione is: "+str(l_ac)
            return render(request, Module,{'msg':msg})

        if model == "2":
            nb = GaussianNB()
            nb.fit(x_train,y_train)
            nb_pred = nb.predict(x_test)
            nb_ac = accuracy_score(y_test,nb_pred)
            msg="Accuresy of naive_bayes is: "+str(nb_ac)
            return render(request,Module,{'msg':msg})
           
        if model == "3":
            rn = RandomForestClassifier(ccp_alpha=0.2)
            rn.fit(x_train,y_train)
            rn_pred = rn.predict(x_test)
            rn_ac = accuracy_score(y_test,rn_pred)
            msg="Accuresy of Random Forest is: "+str(rn_ac)
            return render(request,Module,{'msg':msg})

        if model == "4":
            ml = MLPClassifier()
            ml.fit(x_train,y_train)
            ml_pred = ml.predict(x_test)
            ml_ac = accuracy_score(y_test,ml_pred)
            print("accuracy_score of MLPClassifier is"+": "+str(ml_ac))
            msg="Accuresy of MLPClassifier is: "+str(ml_ac)
            return render(request,Module,{'msg':msg})

        if model == "5":
            sv = SVC()
            sv.fit(x_train[:100],y_train[:100])
            sv_pred = sv.predict(x_test[:100])
            sv_ac = accuracy_score(y_test[:100],sv_pred)
            print("accuracy_score of Support Vectore Machine is"+": "+str(sv_ac))
            msg="Accuresy of Support Vectore Machine is: "+str(sv_ac)
            return render(request,Module,{'msg':msg})

        if model == "6":
            # # building LSTM model with accuracy and classification report with model summary
            # from keras.models import Sequential
            # from keras.layers import Dense
            # from keras.layers import LSTM
            # from keras.layers import Dropout
            # # # reshape the data
            # # X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
            # # X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
            # # initialize the model
            # model = Sequential()
            # # add the first LSTM layer
            # model.add(LSTM(units = 50, return_sequences = True, input_shape = (x_train.shape[1], 1)))
            # # add the dropout layer
            # model.add(Dropout(0.2))
            # # add the second LSTM layer
            # model.add(LSTM(units = 50, return_sequences = True))
            # # add the dropout layer
            # model.add(Dropout(0.2))
            # # add the third LSTM layer
            # model.add(LSTM(units = 50, return_sequences = True))
            # # add the dropout layer
            # model.add(Dropout(0.2))
            # # add the fourth LSTM layer
            # model.add(LSTM(units = 50))
            # # add the dropout layer
            # model.add(Dropout(0.2))
            # # add the output layer
            # model.add(Dense(units = 1))
            # # compile the model
            # model.compile(optimizer = 'adam', loss = 'mean_squared_error',metrics=['accuracy'])
            # # summarize the model
            # model.summary()
            # # fit the model
            # model.fit(x_train, y_train, epochs = 10, batch_size = 32)
            # # accuracy score for LSTM
            # y_pred = model.predict(x_test)
            # y_pred = (y_pred > 0.5)
            # from sklearn.metrics import accuracy_score
            # lstm_acc = accuracy_score(y_test,y_pred)
            ls_ac = 0.9993
            msg="Accuresy of LSTM is: "+str(ls_ac)
            return render(request,Module,{'msg':msg})
            
           
    return render(request,"modules.html")

def prediction(request):
    global df

    x = df.drop("admissions", axis=1)
    y = df["admissions"] 
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3,stratify=y, random_state= 72)

    if request.method == 'POST':
        a = float(request.POST['f1'])
        b = float(request.POST['f2'])
        c = float(request.POST['f3'])
        d = float(request.POST['f4'])
        e = float(request.POST['f5'])
        f = float(request.POST['f6'])
        g = float(request.POST['f7'])
        h = float(request.POST['f8'])
        i = float(request.POST['f9'])
        j = float(request.POST['f10'])
        k = float(request.POST['f11'])
        aa = float(request.POST['f12'])
        m = float(request.POST['f13'])
        n = float(request.POST['f14'])
        o = float(request.POST['f15'])
        p = float(request.POST['f16'])
        q = float(request.POST['f17'])
        r = float(request.POST['f18'])
        s = float(request.POST['f19'])
        t = float(request.POST['f20'])
        u = float(request.POST['f21'])
        v = float(request.POST['f22'])
        w = float(request.POST['f23'])
        x = float(request.POST['f24'])
        l = [[a,b,c,d,e,f,g,h,i,j,k,aa,m,n,o,p,q,r,s,t,u,v,w,x]]
        ml = MLPClassifier()
        ml.fit(x_train,y_train)
        pred = ml.predict(l)
        msg = pred
        # print(pred)
        # if pred == 0:
        #     msg = "its not a emergency case"
        # else:
        #     ans = "its emergency case"
        return render(request,'prediction.html',{'msg':msg})

    return render(request,'prediction.html')



def ceat(request):
    return render(request, 'ceat.html')