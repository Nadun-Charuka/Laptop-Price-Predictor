from flask import Flask,render_template,request
import pickle
import numpy as np
app = Flask(__name__)

def prediction(list):
    filename = 'model/predictor.pickle'
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    pred_value = model.predict([list])
    return pred_value


@app.route('/',methods=['POST','GET'])
def index():
    pred =0
    if request.method == 'POST':
        ram = request.form['ram']
        weight = request.form['weight']
        company = request.form['company']
        typename = request.form['typename']
        opsys = request.form['opsys']
        cpu = request.form['cpuname']
        gpu = request.form['gpuname']
        touchscreen = request.form.getlist('touchscreen')
        ips = request.form.getlist('ips')
        #create a feature list to send to model
        feature_list =[]
        feature_list.append(int(ram))
        feature_list.append(float(weight))
        feature_list.append(len(touchscreen))
        feature_list.append(len(ips))
        #all list of chose
        company_list = ['acer','apple','asus','dell','hp','lenovo','msi','other','toshiba']
        typename_list = ['2in1convertible','gaming','netbook','notebook','ultrabook','workstation']
        opsys_list = ['linux','mac','other','windows']
        cpu_list = ['amd','intelcorei3','intelcorei5','intelcorei7','other']
        gpu_list = ['amd','intel','nvidia']
        #append to list        
        def addToList(list,value):
            for item in list:
                if item == value:
                    feature_list.append(1)
                else:
                    feature_list.append(0)
        addToList(company_list,company)
        addToList(typename_list,typename)
        addToList(opsys_list,opsys)
        addToList(cpu_list,cpu)
        addToList(gpu_list,gpu)
        print(feature_list)

        pred = prediction(feature_list)
        pred = np.round(pred[1])
        print(pred)

    return render_template('index.html',pred = pred)


if __name__ == '__main__':
    app.run(debug=True)