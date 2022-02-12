from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
import time
CORS(app)
import redditUtil

@app.route("/getRedditSentimentChart")
def getSentimentChart():
    #set defaults for arguments
    symbol ='AMZN'
    range ='5y'
    tf = 'all'
    limit = 60
    #get arguments
    tf = request.args.get('time_filter')
    symbol = request.args.get('symbol')
    range = request.args.get('range')
    limit = int(request.args.get('limit'))
    b4time = time.time()
    chartData = redditUtil.getChartData(symbol, range, limit, tf)
    print(time.time()-b4time)
    

    return jsonify(chartData)

if __name__ == "__main__":
  app.run(host="localhost", port=32001, debug=True)