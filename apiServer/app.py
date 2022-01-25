from flask import Flask, request, jsonify
app = Flask(__name__)
import redditUtil

@app.route("/getRedditSentimentChart")
def getSentimentChart():
    #set defaults for arguments
    symbol ='AMZN'
    range ='5y'
    limit = 60
    symbol = request.args.get('symbol')
    range = request.args.get('range')
    limit = int(request.args.get('limit'))
    chartData = redditUtil.getChartData(symbol, range, limit)
    

    return jsonify(chartData)

if __name__ == "__main__":
  app.run(host="localhost", port=32001, debug=True)