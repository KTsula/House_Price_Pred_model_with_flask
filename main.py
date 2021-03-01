import numpy as np
import keras
from flask import Flask , render_template , request , jsonify

app = Flask(__name__)
model = keras.models.load_model('Final_Model_31,7.h5')

@app.route('/')
def home():
     return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
# #     '''
# #     For rendering results on HTML GUI
# #     '''
    first_features = [x for x in request.form.values()]
    entry = []
    parameters = ['ოთახები', 'საერთო ფართი', 'სართული', 'საძინებლები', 'სველი წერტილი',
       'აივანი', 'ცენტრალური გათბობა', 'ბუნებრივი აირი', 'სარდაფი', 'სათავსო',
       'ლიფტი', 'უბანი_აბანოთუბანი', 'უბანი_აეროპორტის გზატ.',
       'უბანი_აეროპორტის დას.', 'უბანი_ავლაბარი', 'უბანი_ავჭალა',
       'უბანი_აფრიკის დას', 'უბანი_ბაგები', 'უბანი_გლდანი',
       'უბანი_დიდი დიღომი', 'უბანი_დიდუბე', 'უბანი_დიღმის მასივი',
       'უბანი_დიღომი 1-9', 'უბანი_ელია', 'უბანი_ვაზისუბანი', 'უბანი_ვაკე',
       'უბანი_ვაჟა ფშაველას კვარტლები', 'უბანი_ვარკეთილი', 'უბანი_ვაშლიჯვარი',
       'უბანი_ვერა', 'უბანი_ვეძისი', 'უბანი_ზაჰესი', 'უბანი_თბილისის ზღვა',
       'უბანი_თემქა', 'უბანი_ივერთუბანი', 'უბანი_ისანი', 'უბანი_კონიაკის დას.',
       'უბანი_კუკია', 'უბანი_ლილო', 'უბანი_ლისის ტბა', 'უბანი_ლოტკინი',
       'უბანი_მესამე მასივი', 'უბანი_მთაწმინდა', 'უბანი_მუხიანი',
       'უბანი_ნავთლუღი', 'უბანი_ნაძალადევი', 'უბანი_ნუცუბიძის ფერდობი',
       'უბანი_ორთაჭალა', 'უბანი_საბურთალო', 'უბანი_სამგორი', 'უბანი_სანზონა',
       'უბანი_სვანეთის უბანი', 'უბანი_სოლოლაკი', 'უბანი_სოფ. გლდანი',
       'უბანი_სოფ. დიღომი', 'უბანი_ფონიჭალა', 'უბანი_ჩუღურეთი',
       'სტატუსი_ახალი აშენებული', 'სტატუსი_მშენებარე',
       'სტატუსი_ძველი აშენებული', 'მდგომარეობა_ახალი რემონტით',
       'მდგომარეობა_გარემონტებული', 'მდგომარეობა_თეთრი კარკასი',
       'მდგომარეობა_მიმდინარე რემონტი', 'მდგომარეობა_მწვანე კარკასი',
       'მდგომარეობა_სარემონტო', 'მდგომარეობა_შავი კარკასი',
       'მდგომარეობა_ძველი რემონტით']
    for i in range (11):
        entry.append(int(first_features[i]))
    
    for i in range (11, 57):
        if first_features[11]==parameters[i][6::]:
            entry.append(1)
        else:
            entry.append(0)

    for i in range (57, 60):
        if first_features[12]==parameters[i][8::]:
            entry.append(1)
        else:
            entry.append(0) 

    for i in range (60, 68):
        if first_features[13]==parameters[i][12::]:
            entry.append(1)
        else:
            entry.append(0) 

    final_features = [(entry)]
    prediction = model.predict(final_features)

# #     output = prediction

    return render_template('index.html', prediction_text='თქვენი ბინის ფასია  {} ლარი'.format(round(prediction[0][0]*10000) ) )


if __name__ == "__main__":
     app.run(debug=True)