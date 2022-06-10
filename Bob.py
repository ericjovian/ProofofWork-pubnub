from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.enums import PNStatusCategory
from pubnub.callbacks import SubscribeCallback
import hashlib, time, os

# replace the key placeholders with your own PubNub publish and subscribe keys
pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-d0918375-2743-4253-a979-d5dd43baf93a'
pnconfig.publish_key = 'pub-c-d1f1acd0-d88b-4d72-8358-579eeb4c47b2'
pnconfig.uuid = "Bob"

pubnub = PubNub(pnconfig)

j = 1
class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, event):
        print("[PRESENCE: {}]".format(event.event))
        print("uuid: {}, channel: {}".format(event.uuid, event.channel))

    def status(self, pubnub, event):
        if event.category == PNStatusCategory.PNConnectedCategory:
            print("[STATUS: PNConnectedCategory]")
            print("connected to channels: {}".format(event.affected_channels))

    def message(self, pubnub, event):
        global j
        fn = str(event.message["ledger_number"])
        blk = event.message["content"]
        ldg =  open("ledger" + fn + ".json","w+")
        ldg.write(blk)
        ldg.close()
        nonce = 500000000
        while nonce < 1000000000:
            cond = (2**236)
            cond = hex(cond)
            #copy the previous block to BobBlock.json to prevent collison with Alice
            file = open("ledger" + fn + ".json","r")
            lines = file.readlines()
            lines[3] = "    \"Nonce\": "+str(nonce)+",\n"
            file = open("BobBlock.json","w+")
            file.writelines(lines)
            file.close()
            #read file
            file = open("BobBlock.json","r")
            data = file.read()
            file.close()
            #hash the data with sha256
            hashval = hashlib.sha256(data.encode()).hexdigest()
            the_message = {"sender": pnconfig.uuid, "content": hashval, "block_number": j, "nonce":nonce}
            if hashval<cond:
                envelope = pubnub.publish().channel('Channel-listenbroadcast').message(the_message).sync()
                nonce = 500000000
                j = j+1
                os.remove('BobBlock.json')
                break
            elif j > 11:
                break
            else:
                #if the data doesn't fulfill the requirement, the nonce will increase by 1
                nonce = nonce+1
                file = open("BobBlock.json","r")
                lines = file.readlines()
                lines[3] = "    \"Nonce\": "+str(nonce)+",\n"
                file = open("BobBlock.json","w+")
                file.writelines(lines)
                file.close()

pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels('Channel-listenmine').with_presence().execute()