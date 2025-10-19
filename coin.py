import requests
import json

class coin:
  def __init__(self):
    self.url="https://api.dexscreener.com/latest/dex/tokens/"

  def update(self,token):
    try:
      self.data=requests.get(self.url+token).json()["pairs"]
    except:
      self.data="server"
      return 1
    else:
      if self.data==None:
        return 1
      else:
        self.data=sorted(self.data,key=lambda x: x.get("liquidity",{}).get("usd",0), reverse=True)
        return 0
      
  def price(self,token):
    self.update(token)
    return f"${self.data[0]["priceUsd"]}"

  def all_pools(self,token):
    self.update(token)
    pools=[{"name": x["dexId"], "liquidity": x.get("liquidity", {}).get("usd", 0.0), "volume_24h": x.get("volume",{}).get("h24",0)} for x in self.data]
    return pools

  def info(self,token):
    self.update(token)
    if self.data==None:
      return {"Unreconized token"}
    elif self.data=="server":
      return {"Server error"}
    coindata={
    "name":self.data[0]["baseToken"]["name"],
    "symbol":self.data[0]["baseToken"]["symbol"],
    "quote":self.data[0]["quoteToken"]["symbol"],
    "price": f"${self.data[0]["priceUsd"]} / {self.data[0]["priceNative"]}{self.data[0]["quoteToken"]["symbol"]}",
    "url": self.data[0]["url"],
    "img": self.data[0].get("info", {}).get("imageUrl", None),
    "website": self.data[0]["info"].get("websites",[])[0].get("url","No website")
    }
    return coindata
  def detail(self,token):
    self.update(token)
    pairs=self.data
    coins_data=[]
    for i in range(0,len(pairs)):
      coin_data={
          "name":pairs[i]["baseToken"]["name"],
          "Liquidity (USD)" : pairs[i].get("liquidity", {}).get("usd", 0.0),
          "Market Cap (USD)": f"${pairs[i].get("marketCap",0)}",
          "24h Volume (USD)": f"${pairs[i]["volume"]["h24"]}",
          "24h buy/sell" : f"{pairs[i]["txns"]["h24"]["buys"]}/{pairs[i]["txns"]["h24"]["sells"]}",
          "24 price change": f"{pairs[i].get("priceChange",{}).get("h24",0)}",
          "Dex": pairs[i]["dexId"],
          "url": pairs[i]["url"]
      }
      coins_data.append(coin_data)

    return coins_data