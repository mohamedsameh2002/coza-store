from django.shortcuts import render

# Create your views here.

def CHAT_PAGE(request):
    return render(request,'communication/chat_page.html')


def ABOUT (request):
    
    return render(request,'communication/about.html')