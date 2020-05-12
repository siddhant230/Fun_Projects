from flask import render_template, redirect, request, url_for, Flask
import wikipedia, random
from collections import defaultdict

app = Flask(__name__)
dic = defaultdict(list)

@app.route('/', methods=["POST", "GET"])
def home():
    global dic
    if request.method == "POST":
        topic = request.form['topic']
        begin = request.form['beginText']

        context = topic + '#' + begin
        topic = context.split('#')[0]

        dic = make_dic(topic)

        return redirect(url_for("display", context=context))
    else:
        return render_template('index.html', content=' ')


def make_dic(topic):
    global dic
    result=wikipedia.summary(topic,sentences=300)
    #perform ngrams

    split_list = result.split(' ')
    keylist = split_list[:-1]
    value_list = split_list[1:]

    for k,v in zip(keylist,value_list):
        dic[k.lower()].append(v.lower())
        print(k, v)

    return dic

turn = True
@app.route('/display<context>', methods=["POST", "GET"])
def display(context):
    global turn

    topic = context.split('#')[0]
    begin = context.split('#')[1]

    if request.method == "POST":
        text = request.form['textall']

        begin = text.split(' ')[-1]
        print(begin)

        if begin in dic:
            new = random.choice(dic[begin])
            final_text = text + ' ' + new
        else:
            new = random.choice(dic[list(dic.keys())[0]])
            final_text = text + ' ' + new

        return render_template('display.html', begin=final_text, topic=topic)

    else:
        return render_template('display.html', begin=begin, topic=topic)


if __name__ == '__main__':
    ip_address = "localhost"
    app.run(host=ip_address, debug=True)
