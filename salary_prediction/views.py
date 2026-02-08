from django.shortcuts import render
import pickle
import numpy as np
import matplotlib.pyplot as plt

from django.conf import settings
from .forms import SalaryForm
from .models import Prediction
import os

#Loading the Model
model_path = os.path.join(
    settings.BASE_DIR,
    'salary_prediction',
    'model',
    'salary_model.pkl',
)
model = pickle.load(open(model_path, 'rb'))

def home(request):
    form = SalaryForm()
    return render(request, 'salary_prediction/home.html', {'form':form})

def predict_salary(request):
    if request.method == 'POST':
        form = SalaryForm(request.POST)

        if form.is_valid():
            exp = form.cleaned_data['experience']

            exp_array = np.array(exp).reshape(-1,1)
            salary = model.predict(exp_array)[0][0]

            Prediction.objects.create(
                experience = exp,
                predict_salary = salary
            )

            #Plot
            x_range = np.linspace(0, 15, 100)
            y_pred = model.predict(x_range.reshape(-1,1))

            plt.figure(figsize=(8,6))
            plt.plot(x_range, y_pred)
            plt.scatter(exp , salary, marker='*')
            plt.ylabel('Years of experience')
            plt.xlabel('Salary (₹)')
            plt.title('LR Prediction Line')

            plot_path = os.path.join(
                settings.MEDIA_ROOT,
                'salary_plot.png'
            )

            plt.savefig(plot_path)
            plt.closer()

            context = {
                'salary' : round(salary, 2),
                'experience': exp,
                'plot_url': settings.MEDIA_URL + 'salary_plot.png'
            }
            return render(request, 'salary_prediction/result.html', context)
        return  render(request, 'salary_prediction/home.html', {'form' : form})