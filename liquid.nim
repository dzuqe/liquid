import os, web3, json

const
  ETH_LINK = "https://mainnet.infura.io/v2/" & getEnv("INFURA_API_KEY")
#  BUCKET_SIZE = 42

var w3 = newWeb3(ETH_LINK)

var f: File = open("/home/hydrogen/dev/dss/out/dapp.sol.json")

#var dss = parseJson(f) 
echo "web3 initialized" 

#var i: int = 0
#var running: bool = true
#while :
#  var s: string = newString(BUCKET_SIZE)
#  if readChars(f,s,i,i+BUCKET_SIZE)!=BUCKET_SIZE:
#    break
#  i += BUCKET_SIZE

