from flask import Flask, render_template, request, redirect
import quandl, requests, pandas as pd, matplotlib.pyplot as plt
import io, base64

app = Flask(__name__)
quandl.ApiConfig.api_key = "kb4sUUo8TQzxWjUbafyQ"

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/hello', methods=['POST'])
def hello():
    tickerID = request.form['tickerID']
    r = requests.get("https://www.quandl.com/api/v3/datasets/WIKI/"+tickerID+".json?start_date=2018-01-01&end_date=2018-12-31&api_key=kb4sUUo8TQzxWjUbafyQ")
    jsonData = (r.json())
    colNames = jsonData['dataset']['column_names']
    tickerData = (jsonData['dataset']['data'])
    df = pd.DataFrame(data=tickerData, columns=colNames)
    img = io.BytesIO()
    plt.plot(df['Adj. Close'])
    plt.title("Closing price trend for " + tickerID + " stock in year 2018")
    plt.xlabel("Date")
    plt.ylabel("Stock Price")
    plt.savefig(img,format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    graph_url = 'data:image/png;base64,{}'.format(graph_url)
    return render_template('chart.html', name=graph_url)

if __name__ == '__main__':
  app.run(port=33507)
