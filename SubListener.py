from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import json

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'sub-c-d0918375-2743-4253-a979-d5dd43baf93a'
pnconfig.publish_key = 'pub-c-d1f1acd0-d88b-4d72-8358-579eeb4c47b2'
pnconfig.uuid = 'Sub'
pubnub = PubNub(pnconfig)

def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        pass  # Message successfully published to specified channel.
    else:
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];

#broadcast the first block
transactions = [ "[3, 4, 5, 6]", "[4, 5, 6, 7]", "[5, 6, 7, 8]", "[6, 7, 8, 9]", "[7, 8, 9, 10]", "[8, 9, 10, 11]", "[9, 10, 11, 12]", "[10, 11, 12, 13]", "[11, 12, 13, 14]", "[12, 13, 14, 15]", "[13, 14, 15, 16]"]
nonce = 0
j=0
tx = json.dumps({"Block number": 0, "Hash": "Genesis", "Nonce": nonce, "Transation": ""}, sort_keys=True, indent=4, separators=(',',': '))
fw = open("block0.json","w+")
fw.write(tx)
fw.close()
the_message = {"sender": pnconfig.uuid, "content": tx, "ledger_number": j}
pubnub.publish().channel('Channel-listenmine').message(the_message).pn_async(my_publish_callback)
prevnonce=[]
nextblock=[]

class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, event):
        print("[PRESENCE: {}]".format(event.event))
        print("uuid: {}, channel: {}".format(event.uuid, event.channel))

    def status(self, pubnub, event):
        if event.category == PNStatusCategory.PNConnectedCategory:
            print("[STATUS: PNConnectedCategory]")
            print("connected to channels: {}".format(event.affected_channels))
    def message(self, pubnub, event):
        global j, nextblock, prevnonce
        cond = (2**236)
        cond = hex(cond)
        # once the sub received a message, it will verify if the hash fulfill the condition.
        if str(event.message["content"]) < cond:
            # print(str(event.message["content"]) + " hash is valid; Mined by: " + str(event.message["sender"])+ " j: "+str(event.message["block_number"]))
            #broadcast new block
            prev = event.message["nonce"]
            nexthash = event.message["content"]
            nextblock.append(nexthash)
            prevnonce.append(prev)
            # comparing alice's and bob's nonce to know who fulfill the requirement first assuming they have the same mining speed
            # the one with less nonce from where they start should be the one mined the block first
            if len(nextblock)==2:
                #broadcast the first mined block based on the nonce's distance from where they start
                if prevnonce[0]<prevnonce[1]:
                    alicenonce = prevnonce[0]
                    bobnonce = prevnonce[1]
                    if (bobnonce - 500000000)> alicenonce:
                        nonce = alicenonce#alice win
                        tx = json.dumps({"Block number": j+1, "Hash": str(nextblock[0]),"Nonce": "", "Transaction": transactions[j]}, sort_keys=True, indent=4, separators=(',',': '))
                        fw = open("block" + str(j+1) + ".json","w+")
                        fw.write(tx)
                        fw.close()
                    else:
                        nonce = bobnonce#bob win
                        tx = json.dumps({"Block number": j+1, "Hash": str(nextblock[1]),"Nonce": "", "Transaction": transactions[j]}, sort_keys=True, indent=4, separators=(',',': '))
                        fw = open("block" + str(j+1) + ".json","w+")
                        fw.write(tx)
                        fw.close()
                    the_message = {"sender": pnconfig.uuid, "content": tx, "ledger_number": j+1}
                    pubnub.publish().channel('Channel-listenmine').message(the_message).pn_async(my_publish_callback)
                    pf = open("block" + str(j) + ".json","r")
                    lines = pf.readlines()
                    lines[3] = "    \"Nonce\": "+str(nonce)+",\n"
                    pf = open("block" + str(j) + ".json","w+")
                    pf.writelines(lines)
                    pf.close()
                    nextblock = []
                    prevnonce = []
                    j = j+1
                else:
                    bobnonce = prevnonce[0]
                    alicenonce = prevnonce[1]
                    if (bobnonce - 500000000)> alicenonce:
                        nonce = alicenonce#alice win
                        tx = json.dumps({"Block number": j+1, "Hash": str(nextblock[1]),"Nonce": "", "Transaction": transactions[j]}, sort_keys=True, indent=4, separators=(',',': '))
                        fw = open("block" + str(j+1) + ".json","w+")
                        fw.write(tx)
                        fw.close()
                    else:
                        nonce = bobnonce#bob win
                        tx = json.dumps({"Block number": j+1, "Hash": str(nextblock[0]),"Nonce": "", "Transaction": transactions[j]}, sort_keys=True, indent=4, separators=(',',': '))
                        fw = open("block" + str(j+1) + ".json","w+")
                        fw.write(tx)
                        fw.close()
                    the_message = {"sender": pnconfig.uuid, "content": tx, "ledger_number": j+1}
                    pubnub.publish().channel('Channel-listenmine').message(the_message).pn_async(my_publish_callback)
                    pf = open("block" + str(j) + ".json","r")
                    lines = pf.readlines()
                    lines[3] = "    \"Nonce\": "+str(nonce)+",\n"
                    pf = open("block" + str(j) + ".json","w+")
                    pf.writelines(lines)
                    pf.close()
                    nextblock = []
                    prevnonce = []
                    j = j+1
            elif len(nextblock)>2:
                nextblock = []
                prevnonce = []
                j = j+1
            else:
                pass
        else:
            pass
            #print(str(event.message["content"]) + " hash is not valid yet; Mined by: " + str(event.message["sender"]))

pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels('Channel-listenbroadcast').with_presence().execute()