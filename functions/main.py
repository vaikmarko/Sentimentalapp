import firebase_functions
from firebase_functions import https_fn
from flask import Flask, request
import functions_framework

# Impordi meie Flask rakendus
from app import app

@functions_framework.http
def app(request):
    """Firebase Cloud Function, mis serveerib meie Flask rakendust."""
    return app(request.environ, lambda x, y: y) 