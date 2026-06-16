from flask import render_template, request,jsonify

def signup():
        return jsonify({
                "code" : 201,
                "message" : "Register Successfully",
                "status": True,
                "error" :[],
                "data" : []
        }),201