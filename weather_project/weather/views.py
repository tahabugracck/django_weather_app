from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

def weather(city):
    link = f"https://havadurumu15gunluk.org/havadurumu/{city}-hava-durumu-15-gunluk.html"
    data = requests.get(link).content
    data = BeautifulSoup(data, "html.parser")
    
    data = data.find("div", {"class": "box weather"})

    try:
        hava_durumu = data.find("span", {"class": "status"}).text.strip()
        sıcaklık = data.find("span", {"class": "temp high bold"}).text.strip()
        hissedilen = data.find("span", {"class": "temp low"}).text.strip()
        
        etiketliler = data.find("ul").find_all("li")
        etiketler = [i.text.strip() for i in etiketliler]
        
        return hava_durumu, sıcaklık, hissedilen, etiketler
    except AttributeError:
        return None, None, None, None

def index(request):
    if request.method == "POST":
        city = request.POST.get("city") 
        hava_durumu, sıcaklık, hissedilen, etiketler = weather(city)
        
        if hava_durumu:
            return render(request, "index.html", {
                "city": city,
                "hava_durumu": hava_durumu,
                "sıcaklık": sıcaklık,
                "hissedilen": hissedilen,
                "etiketler": etiketler
            })
        else:
            error_message = "Hava durumu verisi bulunamadı. Lütfen şehir adını doğru girin."
            return render(request, "index.html", {"error_message": error_message})

    return render(request, "index.html")
