import requests
from collections import defaultdict
import pandas as pd
from time import sleep
pd.options.mode.chained_assignment = None

class Earnings:
    def __init__(self):
        self.avAPI = "8FCG2UU0IWQHWH6G"
        self.k = 1
    def stock_list(self,index="s-and-p-five-hundred"):
        compDF = pd.read_csv("snpCompList.csv")
        print(compDF.columns)
        stockList = compDF["Symbol"].to_list()
        return stockList
    def bySector(self,compList):
        for i in range(0,len(compList)):
            overview = self.overview(compList[i])
            sector = overview["sector"]
    def overview(self,symbol):
        industy = None
        url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={self.avAPI}"
        overview = requests.get(url).json()
        for i in range(0,10):
            try:
                url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={self.avAPI}"
                overview = requests.get(url).json()
                industy = overview["Industry"]
                break
            except:
                sleep(5)
                pass
        # print(overview.keys())
        # sector = overview["Sector"]
        # industry = overview["Industry"]
        return overview
    def earnings(self,symbol):
        quarterly = None
        url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={symbol}&apikey={self.avAPI}'
        
        print(f"{self.k} | {self.k%20}")
        if self.k%20 == 0:
            print(f"{self.k} | sleeping")
        while quarterly is None:
            try:
                edata = requests.get(url).json()
                annual = edata["annualEarnings"]
                quarterly = edata["quarterlyEarnings"]
                self.k+=1
            except:
                pass
        return quarterly 
        #annual = [{fiscalDateEnding: date, reportedEPS: int},{}]
        #quarterly = [{fiscalDateEnding,reportedDate,reportedEPS,estimatedEPS,suprise,suprisePercentage}]
    def edata(self,symbol):
        data = self.earnings(symbol)
        return(data[0])
    def industry(self,series):
        industry = None
        print(self.k)
        if self.k%20==0:
        
            # sleep(10)
            print(f"finish sleep |")
            
        symbol = series.loc["Symbol"]
        print(symbol)
        ov = self.overview(symbol)
        if len(ov.keys()) != 0:
            industry = ov["Industry"]
        print(f"{symbol} | {industry}")
        self.k+=1
        return industry
# a,q = earnings("gme")
# print(q[0].keys())
if __name__ == "__main__":
    e = Earnings()
    # symbol = "googl"
    # g = e.earnings(symbol)
    
    bySector = defaultdict(list)
    byIndustry = defaultdict(list)
    compDF = pd.read_csv("snpCompList.csv")
    # e.industry("aapl")
    # print(compDF.head())
    # compDF = compDF.drop(compDF.index[20:])
    compDF["Industy"] = compDF.apply(e.industry,axis=1)
    compDF.to_csv("snpCompListTest.csv")
    print(compDF.head())
    
    # byIndustry = compDF.groupby(["Industry"])[["Symbol"]]
    # print(byIndustry.groups.keys())
    # energy = bySector.get_group("Energy")
    # energy["lastQ"] = energy.apply(e.earnings,axis=1)
    # print(energy.head())
    #     print(df.head())
        
    
    
    # for i in range(0,25):
    #     overview = e.overview(stockList[i])
    #     sector = overview["Sector"]
    #     industry = overview["Industry"]
    #     bySector[sector].append(stockList[i])
    #     byIndustry[industry].append(stockList[i])
    # print(bySector.keys())