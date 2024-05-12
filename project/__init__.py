from dataclasses import dataclass, field
from flask import Flask,  jsonify, request, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)
app.config.from_object("project.config.Config")
