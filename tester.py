x = {'Results': {'WebServiceOutput0': [{'DiabetesPrediction': 0.0, 'Probability': 0.08922286663087668}]}}
remove_results = str(x['Results'])
diagnosis = remove_results[46:49]
diagnosis_decision = False
if(diagnosis == '1.0'):
    diagnosis_decision = True
diagnosis_probability = str(float(remove_results[66:72])*100) + '%'
print(diagnosis_decision, diagnosis_probability)