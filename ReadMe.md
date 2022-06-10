These code are a simple blockchain system simulating proof-of-work between two parties, Alice and Bob.<br/>
<br/>
to run the program:<br/>
Step 1:<br/>
run Alice.py and Bob.py in different virtual machine<br/>
<h3>&nbsp; ~$ python3 Alice.py<br/></h3>
<h3>&nbsp; ~$ python3 Bob.py<br/></h3>
alice and bob won’t start mining until they receive the first block from sublistener<br/>
<br/>
<br/>
Step 2:<br/>
open terminal on 1 of the computer/virtual machine on the current folder, then run<br/>
SubListener.py first with command:<br/>
<h3>&nbsp; ~$ python3 SubListener.py<br/></h3>
Assuming SubListener is a program running somewhere in the cloud.<br/>
SubListener will broadcast the first genesis block for the miner(Alice and Bob) to mine.<br/>
<br/>
<h4>Make sure you have filled the sub-key and pub-key on all the program.</h4><br.>
<h4>and put the rename the channel1 & channel2 to the channel you hav created on pubnub.</h4>
