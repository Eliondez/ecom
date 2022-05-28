from django.shortcuts import render


def simulation_view(request):
    return render(request, 'simulation/simulation.html')


def base_view(request):
    return render(request, 'simulation/index.html')
