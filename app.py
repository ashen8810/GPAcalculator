from random import randint
import streamlit as st
import csv,os
import json
import requests
from streamlit_lottie import st_lottie
from PIL import Image
import pymongo
from pymongo import MongoClient
client = pymongo.MongoClient("mongodb+srv://admin:*****@cluster0.kqbjq.mongodb.net/******?retryWrites=true&w=majority")
db = client["gpa"]
collection = db["credits"]
collection2 = db["credits2"]



img = Image.open("crest.webp")
st.set_page_config(page_title="GPA Calculator", page_icon=img)

st.title("GPA Calculator")

hide = """
<style>
#MainMenu {visibility : hidden;}

footer {visibility : hidden;}
</style>
"""
import re

st.markdown(hide,unsafe_allow_html=True)
code = """<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=*****"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', '******');
</script>
"""

a=os.path.dirname(st.__file__)+'/static/index.html'
with open(a, 'r') as f:
    data=f.read()
    if len(re.findall('G-', data))==0:
        with open(a, 'w') as ff:
            newdata=re.sub('<head>','<head>'+code,data)
            ff.write(newdata)

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


lottie_coding = load_lottiefile("lottiefile.json")
l = load_lottiefile("l.json")
st_lottie(l,
          height=250,
          width=250
          )
if "sem1" not in st.session_state or "sem2" not in st.session_state:
    st_lottie(
        lottie_coding,
        speed=1.2,
        reverse=False,
        loop=True,
        quality="high"  # medium ; high

    )

    test = collection.find({})

    rows1 = []
    rows2 = []

    for i in test:
        rows1.append(i["course"])
        rows2.append(i["credit"])


    st.session_state.sem1 = {}
    for key in rows1:
        for value in rows2:
            st.session_state.sem1[key] = int(value)
            rows2.remove(value)
            break
    i=2
    rows1 = []
    rows2 = []
    test = collection2.find({})

    for i in test:
        rows1.append(i["course"])
        rows2.append(i["credit"])

    st.session_state.sem2 = {}
    for key in rows1:
        for value in rows2:
            st.session_state.sem2[key] = int(value)
            rows2.remove(value)
            break


grading_scale = {"A+" : 4, "A" : 4, "A-" : 3.7, "B+" : 3.3, "B" : 3.0, "B-" : 2.7, "C+" : 2.3, "C" : 2.0, "C-" : 1.7, "D" : 1.3, "D-" : 1.0, "E" : 0 }
grades = []
courses1= []
courses2= []

for i in st.session_state.sem1:
    courses1.append(i)
for i in st.session_state.sem2:
    courses2.append(i)
for j in grading_scale:
    grades.append(j)
if "rn" not in st.session_state:
    st.session_state.rn = randint(0, 1000)
radiobtton = st.radio("Semester",["1","2"])

if radiobtton == "1":
    with st.form("form1"):
        filename = str(st.session_state.rn) + "gpa.csv"
        c1 = st.selectbox("Course",st.session_state.sem1)
        c1g = st.selectbox("Grade",grades)
        submit = st.form_submit_button("Submit")
        if submit == True:
            with open(filename,"a",newline = "") as f:
                writer = csv.writer(f)
                writer.writerow([c1,c1g])
            with open(filename,"r") as f:
                    reader = csv.reader(f)
                    for row in reader:
                        marks = row[0]+"\t----->"+ row[1]
                        st.markdown(marks)

    clear = st.button("Clear")
    if clear == True:
        try:
            os.remove(filename)
            st.success("Done")
        except:
            st.write("Done")

    f = st.button("Calculate GPA")
    if f == True:

        try:
            with open(filename, "r") as f:
                reader = csv.reader(f)
                i = 0
                csum = 0
                gpsum = 0
                keys = []
                values = []
                di = {}

                for row in reader:
                    marks = row[0] + "\t-" + row[1]
                    di[row[0]] = [float(grading_scale[row[1]]),float(st.session_state.sem1[row[0]])]
                    i = i + 1
            for i in di:
                # gpsum = gpsum + int(i[1])
                csum = csum+di[i][1]
                gpsum = gpsum+ di[i][0]*di[i][1]


            gpa = "Your GPA is  : " + str(gpsum / csum)
            st.header(gpa)
            st.write("Total Credits -> " + str(int(csum)))

            st.balloons()
            os.remove(filename)


        except FileNotFoundError:

            st.warning("Please Fill the data")

        except:
            os.remove(filename)


else:
    with st.form("form2"):
        filename = str(st.session_state.rn) + "gpa.csv"

        c1 = st.selectbox("Course",st.session_state.sem2)
        c1g = st.selectbox("Grade", grades)
        submit = st.form_submit_button("Submit")
        if submit == True:
            from random import randint
            with open(filename, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([c1, c1g])
            with open(filename, "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    marks = row[0] + "\t----->" + row[1]
                    st.markdown(marks)

    clear = st.button("Clear")
    if clear == True:
        try:
            os.remove(filename)
            st.success("Done")
        except:
            st.write("Done")

    f = st.button("Calculate GPA")
    if f == True:
        try:
            with open(filename, "r") as f:
                reader = csv.reader(f)
                i = 0
                csum = 0
                gpsum = 0
                keys = []
                values = []
                di = {}

                for row in reader:
                    marks = row[0] + "\t-" + row[1]
                    di[row[0]] = [float(grading_scale[row[1]]),float(st.session_state.sem2[row[0]])]
                    i = i + 1
            for i in di:
                # gpsum = gpsum + int(i[1])
                csum = csum+di[i][1]
                gpsum = gpsum+ di[i][0]*di[i][1]


            gpa = "Your GPA is  : " + str(gpsum / csum)
            st.header(gpa)
            st.write("Total Credits -> " + str(int(csum)))

            st.balloons()
            os.remove(filename)


        except FileNotFoundError:

            st.warning("Please Fill the data")

        except:
            os.remove(filename)
