from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.enums import PNStatusCategory
from pubnub.callbacks import SubscribeCallback
import hashlib, time, os

# replace the key placeholders with your own PubNub publish and subscribe keys
pnconfig = PNConfiguration()
pnconfig.subscribe_key = #your pubnub's app subscribe key
pnconfig.publish_key = #your pubnub's app publish key
pnconfig.uuid = "Alice"

pubnub = PubNub(pnconfig)

class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, event):
        print("[PRESENCE: {}]".format(event.event))
        print("uuid: {}, channel: {}".format(event.uuid, event.channel))

    def status(self, pubnub, event):
        if event.category == PNStatusCategory.PNConnectedCategory:
            print("[STATUS: PNConnectedCategory]")
            print("connected to channels: {}".format(event.affected_channels))

    def message(self, pubnub, event):
        fn = str(event.message["ledger_number"])
        blk = event.message["content"]
        ldg =  open("ledger" + fn + ".json","w+")
        ldg.write(blk)
        ldg.close()
        nonce = 0
        while nonce < 1000000000:
            cond = (2**236)
            cond = hex(cond)
            #copy the previous block to AliceBlock.json to prevent collison with Bob
            file = open("ledger" + fn + ".json","r")
            lines = file.readlines()
            lines[3] = "    \"Nonce\": "+str(nonce)+",\n"
            file = open("AliceBlock.json","w+")
            file.writelines(lines)
            file.close()
            #read file
            file = open("AliceBlock.json","r")
            data = file.read()
            file.close()
            #hash the datas
            hashval = hashlib.sha256(data.encode()).hexdigest()
            the_message = {"sender": pnconfig.uuid, "content": hashval, "nonce":nonce}
            if hashval < cond:
                envelope = pubnub.publish().channel('channel1').message(the_message).sync()
                nonce = 0
                os.remove("AliceBlock.json")
                break
            else:
                #if the data doesn't fulfill the requirement, the nonce will increase by 1
                nonce = nonce+1
                file = open("AliceBlock.json","r")
                lines = file.readlines()
                lines[3] = "    \"Nonce\": "+str(nonce)+",\n"
                file = open("AliceBlock.json","w+")
                file.writelines(lines)
                file.close()

pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels("channel2").with_presence().execute()
