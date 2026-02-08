from django.shortcuts import render
from django.conf import settings
from .forms import SalaryForm
from .models import Prediction

import pickle
import numpy as np
import matplotlib.pyplot as plt
import os


# Load ML model once
model_path = os.path.join(
    settings.BASE_DIR,
    'salary_prediction',
    'model',
    'salary_model.pkl'
)

with open(model_path, 'rb') as f:
    model = pickle.load(f)


def home(request):
    form = SalaryForm()
    return render(request, 'salary_prediction/home.html', {'form': form})


def predict_salary(request):
    if request.method == 'POST':
        form = SalaryForm(request.POST)

        if form.is_valid():
            exp = form.cleaned_data['experience']

            exp_array = np.array(exp).reshape(-1, 1)
            predicted_salary = model.predict(exp_array)[0][0]

        
            Prediction.objects.create(
                experience=exp,
                predicted_salary=predicted_salary
            )

            # Plot
            x_range = np.linspace(0, 15, 100)
            y_pred = model.predict(x_range.reshape(-1, 1))

            plt.figure(figsize=(8, 6))
            plt.plot(x_range, y_pred, label='Prediction Line')
            plt.scatter(exp, predicted_salary, color='red', marker='*', label='Input')
            plt.xlabel('Years of Experience')
            plt.ylabel('Salary (₹)')
            plt.title('Salary Prediction')
            plt.legend()

            plot_path = os.path.join(settings.MEDIA_ROOT, 'salary_plot.png')
            plt.savefig(plot_path)
            plt.close()

            context = {
                'experience': exp,
                'salary': round(predicted_salary, 2),
                'plot_url': settings.MEDIA_URL + 'salary_plot.png'
            }

            return render(request, 'salary_prediction/result.html', context)

    
    form = SalaryForm()
    return render(request, 'salary_prediction/home.html', {'form': form})