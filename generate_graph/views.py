from django.shortcuts import render

def account_info(request):
    # Chemin d'accès au graphique généré
    chart_path = "/static/charts/format_distribution.png"
    return render(request, "account/account_info.html", {"chart_path": chart_path})
