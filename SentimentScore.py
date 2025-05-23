import json
import csv
import urllib.request

txtfile = open('output.txt', 'w')

def get_jsonparsed_data(url):
    with urllib.request.urlopen(url) as response:
        data = response.read()
        return json.loads(data.decode())

def getObj(url):
    return get_jsonparsed_data(url)

# Attain APIKey from this website https://www.alphavantage.co/support/#api-key and paste into string
apiKey = ""

# Set start and end date for "past" analysis
# Time from Sept 2024 to Dec 2024
startDate1 = "20240901T0130"
endDate1 = "20241201T0130"

# Set 2nd start date, will collect data all the way to the present
# Time from Jan 2025 to present
startDate2 = "20250104T0130"

# List of tickers that will be analyzed (max 12)
listOfTickers = ["CZR", "SONY", "TSLA", "LAZ", "MS", "UBS", "ILMN", "IQV", "ASML", "MSFT", "NOW", "NVDA"]
    

txtfile.write("https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=" + "NVDA" + "&limit=1000&time_from=" + startDate1 + "&time_to=" + endDate1 + "&apikey=" + apiKey)
def generateCsvs(selectedTicker):
    
    
    pastObj = getObj("https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=" + selectedTicker + "&limit=1000&time_from=" + startDate1 + "&time_to=" + endDate1 + "&apikey=" + apiKey)
    presentObj = getObj("https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=" + selectedTicker + "&limit=1000&time_from=" + startDate2 + "&apikey=" + apiKey)
    
    def findSentAvg(tickerSymbol, obj):
            j = 0
            sentScoreAvg = 0.0
            for item in obj["feed"]:
                print(selectedTicker)
                for ticker in item["ticker_sentiment"]:
                    if ticker["ticker"] == tickerSymbol:
                        sentScoreAvg += float(ticker["ticker_sentiment_score"])
                        j += 1
            if j == 0:
                return 0.0, 0  # Prevent division by zero
            sentScoreAvg /= j
            return sentScoreAvg, j
    
    def generateResult(obj, nameOfFile):
        print(obj)
        
        verbalRating = ""
        
            
        
        sentScoreAvg, j = findSentAvg(selectedTicker, obj)
        
        ratingsFound = j
                
        if sentScoreAvg <= -0.35:
            verbalRating = "Bearish"
        elif -0.35 < sentScoreAvg <= -0.15:
            verbalRating = "Somewhat Bearish"
        elif -0.15 < sentScoreAvg < 0.15:
            verbalRating = "Neutral"
        elif 0.15 <= sentScoreAvg < 0.35:
            verbalRating = "Somewhat Bullish"
        else:
            verbalRating = "Bullish"
        
        returnArr = [sentScoreAvg, ratingsFound, verbalRating]
        return returnArr
    
    print(selectedTicker)
    
    returnArrPast = generateResult(pastObj, "pastSentiment")
    returnArrPresent = generateResult(presentObj, "presentSentiment")
    return returnArrPast,returnArrPresent



returnArr = []
sentScoreAvgPast = []
ratingsFoundPast = []
verbalRatingPast = []

sentScoreAvgPresent = []
ratingsFoundPresent = []
verbalRatingPresent = []

changeInSentiment = []

for i in range(len(listOfTickers)):
    newSentScoreAvg = 0.0
    newRatingFound = 0
    newVerbalRating = ""
    
    returnArrPast,returnArrPresent = generateCsvs(listOfTickers[i])
   
    sentScoreAvgPast.append(returnArrPast[0])
    ratingsFoundPast.append(returnArrPast[1])
    verbalRatingPast.append(returnArrPast[2])
    
    sentScoreAvgPresent.append(returnArrPresent[0])
    ratingsFoundPresent.append(returnArrPresent[1])
    verbalRatingPresent.append(returnArrPresent[2])
    
    changeInSentiment.append((sentScoreAvgPresent[i] - sentScoreAvgPast[i])/(sentScoreAvgPast[i] + 0.000000001))
    
    txtfile.write("\n" + "Analysis for " + listOfTickers[i]+ "\n")
    txtfile.write(startDate1 + " numerical sentiment: " + str(sentScoreAvgPast[i]) + "\n")
    txtfile.write(startDate1 + " number of ratings found: " + str(ratingsFoundPast[i])+ "\n")
    txtfile.write(startDate1 + " investor sentiment: " + str(verbalRatingPast[i])+ "\n")
    txtfile.write("\n")
    txtfile.write(startDate2 + " numerical sentiment: " + str(sentScoreAvgPresent[i])+ "\n")
    txtfile.write(startDate2 + " number of ratings found: " + str(ratingsFoundPresent[i])+ "\n")
    txtfile.write(startDate2 + " investor sentiment: " + str(verbalRatingPresent[i])+ "\n")
    txtfile.write("\n")
    txtfile.write("Change in sentiment: " + str(changeInSentiment[i] * 100) + "%"+ "\n" )
    txtfile.write("\n")
    txtfile.write("\n")
    
with open("analysis" + ".csv", 'w', newline="") as f:
    csvWriter = csv.writer(f)
    csvWriter.writerow(["Ticker", "Sentiment Score Avg Past", "Sentiment Score Avg Present", "Change in Sentiment (%)", "Investor Sentiment Past", "Investor Sentiment Present", "Ratings Found Past", "Ratings Found Present"])
    for i in range(len(listOfTickers)):
        txtfile.write(str(i))
        txtfile.write(str(ratingsFoundPresent[i]))
        csvWriter.writerow([listOfTickers[i], sentScoreAvgPast[i], sentScoreAvgPresent[i], changeInSentiment[i] * 100, verbalRatingPast[i], verbalRatingPresent[i], ratingsFoundPast[i], ratingsFoundPresent[i]])