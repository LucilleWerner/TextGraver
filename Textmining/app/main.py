#! /usr/bin/env python

from flask import Flask, render_template, send_from_directory, flash, request, redirect, url_for, g, Response
from app import app
import simplejson as json

@app.route("/")
def index():
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')


@app.route("/reports", methods=["POST", "GET"])
def reports():
    trail = request.args.get("keyword")
    trail = "http://eggnogapi.embl.de/nog_data/html/tree/"+trail
    return render_template('reports.html', trail=trail)



@app.route("/charts", methods=["POST", "GET"])
def charts():
    trail = request.args.get('keyword')
    return render_template('charts.html', trail=trail)


@app.route("/sunburst")
def sunburst():
    return render_template('sunburst.html')

@app.route("/graph")
def graph():

    return render_template('graph.html')


@app.route("/error")
def error():
    return render_template('error.html')

@app.route("/flowchart")
def flowchart():
    return render_template('flowchart.html')

@app.route("/api")
def api():
    return render_template('api.html')


@app.route("/term")
def term():
    trail = request.args.get('search')

    return render_template('linking.html', term=trail)


@app.route("/graph_green")
def graph_green():
    return render_template('graph_green.html')

@app.route("/graph_red")
def graph_red():
    return render_template('graph_red.html')

@app.route("/graph_blue")
def graph_blue():
    return render_template('graph_blue.html')

@app.route("/graph_gray")
def graph_gray():
    return render_template('graph_gray.html')

@app.route("/graph_purple")
def graph_purple():
    return render_template('graph_purple.html')

@app.route("/graph_lowtemperature")
def graph_lowtemperature():
    return render_template('graph_lowtemperature.html')



@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'),404
