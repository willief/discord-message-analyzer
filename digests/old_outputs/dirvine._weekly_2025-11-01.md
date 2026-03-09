# dirvine. Weekly Digest

*Week of 2025-10-25 to 2025-11-01*

*Generated: 2025-11-01 23:44:34 UTC*

**Messages this week: 30**

This digest contains dirvine.'s recent posts and replies to their messages.

---


## Sunday, 2025-10-26

**[#🌐︱general-chat]** `18:48:06` **dirvine.** said:

It does have mobile capabilities, but we are also providing swift and kotlin API's. Tauri v2 has a couple of small release issues right now (tauri build needs to be updated to 2.9 where it's only 2.5 and tauri is at 2.9, we don't control that). 

So to be clear tauri is able to run on mobile, but it's not write once run everywhere at all, you do need to repliment the front end for mobile, so you need a frontend for each plartofrm and use tauri to wrap it, otherwise you jsut go for it and use swift and kotlin. Not a simple choice, but it is a choice.

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1432078356320616643)

---


### 💬 dirvine. posted

**[#🌐︱general-chat]** `18:48:06`

**dirvine.**: It does have mobile capabilities, but we are also providing swift and kotlin API's. Tauri v2 has a couple of small release issues right now (tauri build needs to be updated to 2.9 where it's only 2.5 and tauri is at 2.9, we don't control that). 

So to be clear tauri is able to run on mobile, but it's not write once run everywhere at all, you do need to repliment the front end for mobile, so you need a frontend for each plartofrm and use tauri to wrap it, otherwise you jsut go for it and use swift and kotlin. Not a simple choice, but it is a choice.

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1432078356320616643)

---


## Tuesday, 2025-10-28

**[#🎫︱general-support]** `09:18:24` **dirvine.** said:

It's a valid thought experiment we need to check for sure. Nice one

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1432659761802772510)

---


### 💬 dirvine. posted

**[#🎫︱general-support]** `09:18:24`

**dirvine.**: It's a valid thought experiment we need to check for sure. Nice one

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1432659761802772510)

---

**[#🎫︱general-support]** `10:29:41` **dirvine.** said:

For CRDT, there is no real wrong copy. There are older copies, and they are always valuable until you get a newer copy. I'm not sure all of our clients are following the CRDT methodology correctly. However, what should be happening is you get as many copies as you possibly can. You use the latest copy, so the highest vector clock, but also you should publish that latest copy back to everybody that gave you an older copy.

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1432677699519905812)

---


### 💬 dirvine. posted

**[#🎫︱general-support]** `10:29:41`

**dirvine.**: For CRDT, there is no real wrong copy. There are older copies, and they are always valuable until you get a newer copy. I'm not sure all of our clients are following the CRDT methodology correctly. However, what should be happening is you get as many copies as you possibly can. You use the latest copy, so the highest vector clock, but also you should publish that latest copy back to everybody that gave you an older copy.

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1432677699519905812)

---

**[#🎫︱general-support]** `18:25:08` **dirvine.** said:

> I also think we can't trust clients, only nodes. Clients don't have enough skin in the game. Maybe clients/nodes are being used interchangeably above though?
This is correct but what we're talking about here is data on this network, so it's either immutable and self-referential. Or it's signed by the owner. So it's not like we're trusting clients here in any way where they can create new data or whatever. 

It's not about trust, we've sort of removed the trust element here. So data is either signed by the owner (and correct) or it's self-referential (and correct). Anything else is incorrect and would not be stored. 

It's these subtle areas where I think the scratchpad could be really abused though. The scratchpad intention was literally a place for apps to write config data or other unstructured data, but I think, maybe it's correct and people are following the rules, scratchpads could be really stretched out to hold actual information. Actually, this is not secure and isn't following CRDT patterns, etc. I try and keep my eye on that, but it's not straightforward. It's not really up to us to force a particular use of an API. If the API is here, folks should be able to use it whatever way they possibly feel they can.

If we really don't want something to happen, it shouldn't be in our API to have the ability to do that. Scratchpads are definitely a grey area, where there's grey, there's probably confusion. It's really difficult because it's that mix of trying to do something that's a little bit more flexible, and then people take that flexibility and push it to the absolute extreme. I'm not saying anybody's right or anybody's wrong, I'm just noting that.

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1432797350191169588)

---


### 💬 dirvine. posted

**[#🎫︱general-support]** `18:25:08`

**dirvine.**: > I also think we can't trust clients, only nodes. Clients don't have enough skin in the game. Maybe clients/nodes are being used interchangeably above though?
This is correct but what we're talking about here is data on this network, so it's either immutable and self-referential. Or it's signed by the owner. So it's not like we're trusting clients here in any way where they can create new data or whatever. 

It's not about trust, we've sort of removed the trust element here. So data is either signed by the owner (and correct) or it's self-referential (and correct). Anything else is incorrect and would not be stored. 

It's these subtle areas where I think the scratchpad could be really abused though. The scratchpad intention was literally a place for apps to write config data or other unstructured data, but I think, maybe it's correct and people are following the rules, scratchpads could be really stretched out to hold actual information. Actually, this is not secure and isn't following CRDT patterns, etc. I try and keep my eye on that, but it's not straightforward. It's not really up to us to force a particular use of an API. If the API is here, folks should be able to use it whatever way they possibly feel they can.

If we really don't want something to happen, it shouldn't be in our API to have the ability to do that. Scratchpads are definitely a grey area, where there's grey, there's probably confusion. It's really difficult because it's that mix of trying to do something that's a little bit more flexible, and then people take that flexibility and push it to the absolute extreme. I'm not saying anybody's right or anybody's wrong, I'm just noting that.

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1432797350191169588)

---

**[#🎫︱general-support]** `19:06:17` **traktion0_20257** replied to dirvine.:

> *dirvine. said:*
> > I also think we can't trust clients, only nodes. Clients don't have enough skin in the game. Maybe clients/nodes are being used interchangeably above though?
This is correct but what we're talking about here is data on this network, so it's either immutable and self-referential. Or it's signed by the owner. So it's not like we're trusting clients here in any way where they can create new data or whatever. 

It's not about trust, we've sort of removed the trust element here. So data is either signed by the owner (and correct) or it's self-referential (and correct). Anything else is incorrect and would not be stored. 

It's these subtle areas where I think the scratchpad could be really abused though. The scratchpad intention was literally a place for apps to write config data or other unstructured data, but I think, maybe it's correct and people are following the rules, scratchpads could be really stretched out to hold actual information. Actually, this is not secure and isn't following CRDT patterns, etc. I try and keep my eye on that, but it's not straightforward. It's not really up to us to force a particular use of an API. If the API is here, folks should be able to use it whatever way they possibly feel they can.

If we really don't want something to happen, it shouldn't be in our API to have the ability to do that. Scratchpads are definitely a grey area, where there's grey, there's probably confusion. It's really difficult because it's that mix of trying to do something that's a little bit more flexible, and then people take that flexibility and push it to the absolute extreme. I'm not saying anybody's right or anybody's wrong, I'm just noting that.

Right, understood. So, it's more that clients can advertise their signed mutable data, to make others aware of it. They can't change it, as the signature would be invalidated. 👍

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1432807705260720260)

---


### 💭 Reply to dirvine.

**[#🎫︱general-support]** `19:06:17`

↳ *dirvine. said:*
> > I also think we can't trust clients, only nodes. Clients don't have enough skin in the game. Maybe clients/nodes are being used interchangeably above though?
This is correct but what we're talking about here is data on this network, so it's either immutable and self-referential. Or it's signed by the owner. So it's not like we're trusting clients here in any way where they can create new data or whatever. 

It's not about trust, we've sort of removed the trust element here. So data is either signed by the owner (and correct) or it's self-referential (and correct). Anything else is incorrect and would not be stored. 

It's these subtle areas where I think the scratchpad could be really abused though. The scratchpad intention was literally a place for apps to write config data or other unstructured data, but I think, maybe it's correct and people are following the rules, scratchpads could be really stretched out to hold actual information. Actually, this is not secure and isn't following CRDT patterns, etc. I try and keep my eye on that, but it's not straightforward. It's not really up to us to force a particular use of an API. If the API is here, folks should be able to use it whatever way they possibly feel they can.

If we really don't want something to happen, it shouldn't be in our API to have the ability to do that. Scratchpads are definitely a grey area, where there's grey, there's probably confusion. It's really difficult because it's that mix of trying to do something that's a little bit more flexible, and then people take that flexibility and push it to the absolute extreme. I'm not saying anybody's right or anybody's wrong, I'm just noting that.

**traktion0_20257**: Right, understood. So, it's more that clients can advertise their signed mutable data, to make others aware of it. They can't change it, as the signature would be invalidated. 👍

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1432807705260720260)

---


## Wednesday, 2025-10-29

**[#🎫︱general-support]** `11:42:01` **dirvine.** said:

This conversation above referenced chunks, scratch pads and pointers, mutable and immutable data. Scratch pads and pointers are different items. Same as chunks are different. The ability to misuse should not be characterised in any negative way from what I've said. When people design an API, they design it for a particular use, and they hope that it meets that use. The better the API, the harder it is to use, different from what was anticipated. It's not black and white, it's not binary. Love, hate. 
API design is a very tricky thing, and the more flexibility you try and provide with an API, the more use cases it can be used for, obviously. 

Sometimes those use cases are unintended; sometimes that could be a brilliant thing; and sometimes it could be a troublesome thing.

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433058288961982557)

---


### 💬 dirvine. posted

**[#🎫︱general-support]** `11:42:01`

**dirvine.**: This conversation above referenced chunks, scratch pads and pointers, mutable and immutable data. Scratch pads and pointers are different items. Same as chunks are different. The ability to misuse should not be characterised in any negative way from what I've said. When people design an API, they design it for a particular use, and they hope that it meets that use. The better the API, the harder it is to use, different from what was anticipated. It's not black and white, it's not binary. Love, hate. 
API design is a very tricky thing, and the more flexibility you try and provide with an API, the more use cases it can be used for, obviously. 

Sometimes those use cases are unintended; sometimes that could be a brilliant thing; and sometimes it could be a troublesome thing.

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433058288961982557)

---

**[#🎫︱general-support]** `12:01:38` **toivo_toivo** replied to dirvine.:

> *dirvine. said:*
> This conversation above referenced chunks, scratch pads and pointers, mutable and immutable data. Scratch pads and pointers are different items. Same as chunks are different. The ability to misuse should not be characterised in any negative way from what I've said. When people design an API, they design it for a particular use, and they hope that it meets that use. The better the API, the harder it is to use, different from what was anticipated. It's not black and white, it's not binary. Love, hate. 
API design is a very tricky thing, and the more flexibility you try and provide with an API, the more use cases it can be used for, obviously. 

Sometimes those use cases are unintended; sometimes that could be a brilliant thing; and sometimes it could be a troublesome thing.

Yeah, I didn't think the "misuse" as a negative, just finding more, and more and more than most prominently intended use case.

But about behaviour Traktion saw when getting  the 3 different results. Is that expected and correct? If not, is it more user error or something to be improved on the network side?

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433063227125928097)

---


### 💭 Reply to dirvine.

**[#🎫︱general-support]** `12:01:38`

↳ *dirvine. said:*
> This conversation above referenced chunks, scratch pads and pointers, mutable and immutable data. Scratch pads and pointers are different items. Same as chunks are different. The ability to misuse should not be characterised in any negative way from what I've said. When people design an API, they design it for a particular use, and they hope that it meets that use. The better the API, the harder it is to use, different from what was anticipated. It's not black and white, it's not binary. Love, hate. 
API design is a very tricky thing, and the more flexibility you try and provide with an API, the more use cases it can be used for, obviously. 

Sometimes those use cases are unintended; sometimes that could be a brilliant thing; and sometimes it could be a troublesome thing.

**toivo_toivo**: Yeah, I didn't think the "misuse" as a negative, just finding more, and more and more than most prominently intended use case.

But about behaviour Traktion saw when getting  the 3 different results. Is that expected and correct? If not, is it more user error or something to be improved on the network side?

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433063227125928097)

---

**[#🎫︱general-support]** `12:06:20` **dirvine.** said:

There is an issue in the network for sure, @QiMa spotted it and relates to crdt vector clocks etc. Howevre clients also need to do some work here too. its just CRDT.

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433064412540829788)

---


### 💬 dirvine. posted

**[#🎫︱general-support]** `12:06:20`

**dirvine.**: There is an issue in the network for sure, @QiMa spotted it and relates to crdt vector clocks etc. Howevre clients also need to do some work here too. its just CRDT.

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433064412540829788)

---

**[#🎫︱general-support]** `12:07:20` **toivo_toivo** replied to dirvine.:

> *dirvine. said:*
> There is an issue in the network for sure, @QiMa spotted it and relates to crdt vector clocks etc. Howevre clients also need to do some work here too. its just CRDT.

Did @Traktion possibly make some concurrent updates to cause some forking?

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433064662051717274)

---


### 💭 Reply to dirvine.

**[#🎫︱general-support]** `12:07:20`

↳ *dirvine. said:*
> There is an issue in the network for sure, @QiMa spotted it and relates to crdt vector clocks etc. Howevre clients also need to do some work here too. its just CRDT.

**toivo_toivo**: Did @Traktion possibly make some concurrent updates to cause some forking?

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433064662051717274)

---

**[#🎫︱general-support]** `12:08:14` **dirvine.** said:

Possibly, I am not sure though, he has a good grasp on things so I am not sure

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433064887411675266)

---


### 💬 dirvine. posted

**[#🎫︱general-support]** `12:08:14`

**dirvine.**: Possibly, I am not sure though, he has a good grasp on things so I am not sure

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433064887411675266)

---


## Thursday, 2025-10-30

**[#🌐︱general-chat]** `17:25:03` **dirvine.** said:

We have to make it so. There are a few tweaks and things happening at the moment, but let's make sure we get this into the client library.

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1433507007578505276)

---


### 💬 dirvine. posted

**[#🌐︱general-chat]** `17:25:03`

**dirvine.**: We have to make it so. There are a few tweaks and things happening at the moment, but let's make sure we get this into the client library.

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1433507007578505276)

---

**[#🎫︱general-support]** `19:33:03` **dirvine.** said:

The network was originally envisaged to be apps running nodes. So everyones computer was a node and they all connected in a large network. Life moved on, mobiles happened, cloud happened and many other things. Anyway we ended up with node runners that means folks not running apps, but just running nodes. 
Some folk running nodes for pure profit will do any amount of harm to others or the network to make a single $0.000001 for themselves. This is the. game we are currently in. It is how it is, people will take everything and leave nothing, given the chance. Not all peopel by any means, but we are the special species that will harm each other cause we can 😉 

However we need to consider this sort of thing more, emissions are a tool to help node runners as we get off the ground, that is takign longer than we wanted, but great progress is being made. 

I think we will be pulled to pieces until we are off the ground, jsut as the bitcoin network would have at teh start, had more folk acted in the extreme greed mode, but the original bitcoin crowd were very different to the new crows in these projects now, that's just how it is. 

I think this is great to report @Dimitar and I hope it's not cost you personally. I don't totally blame that guy, but I am not suprised, the loud accusing voices tend to be the very folks gaming the system as he was. They get a lot of ego boosting from sidelining us and fake reporting other stuff etc. It's also why I get annoyed when we see folk screaming about whales and other folk getting rewards, there is often another reason behind that kind of screaming and shouting.  It's another thing we need to take care off as folk report stuff. They are not always honest 😉  (our community has tended to believe most folk and take them at face value, I am not so inclined to do that any more)

Anyway, it's something to fix for sure, the nodes not behaving for sure need to be cleared out of the network quickly. It is an area where staking does help where bad actors lose stakes. Kinda sad, but true.

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433539218067558430)

---


### 💬 dirvine. posted

**[#🎫︱general-support]** `19:33:03`

**dirvine.**: The network was originally envisaged to be apps running nodes. So everyones computer was a node and they all connected in a large network. Life moved on, mobiles happened, cloud happened and many other things. Anyway we ended up with node runners that means folks not running apps, but just running nodes. 
Some folk running nodes for pure profit will do any amount of harm to others or the network to make a single $0.000001 for themselves. This is the. game we are currently in. It is how it is, people will take everything and leave nothing, given the chance. Not all peopel by any means, but we are the special species that will harm each other cause we can 😉 

However we need to consider this sort of thing more, emissions are a tool to help node runners as we get off the ground, that is takign longer than we wanted, but great progress is being made. 

I think we will be pulled to pieces until we are off the ground, jsut as the bitcoin network would have at teh start, had more folk acted in the extreme greed mode, but the original bitcoin crowd were very different to the new crows in these projects now, that's just how it is. 

I think this is great to report @Dimitar and I hope it's not cost you personally. I don't totally blame that guy, but I am not suprised, the loud accusing voices tend to be the very folks gaming the system as he was. They get a lot of ego boosting from sidelining us and fake reporting other stuff etc. It's also why I get annoyed when we see folk screaming about whales and other folk getting rewards, there is often another reason behind that kind of screaming and shouting.  It's another thing we need to take care off as folk report stuff. They are not always honest 😉  (our community has tended to believe most folk and take them at face value, I am not so inclined to do that any more)

Anyway, it's something to fix for sure, the nodes not behaving for sure need to be cleared out of the network quickly. It is an area where staking does help where bad actors lose stakes. Kinda sad, but true.

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433539218067558430)

---

**[#🌐︱general-chat]** `19:45:26` **dirvine.** said:

The gas is actually paid in the autonomi token so you don't need ETH tokens at all?

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1433542334993137664)

---


### 💬 dirvine. posted

**[#🌐︱general-chat]** `19:45:26`

**dirvine.**: The gas is actually paid in the autonomi token so you don't need ETH tokens at all?

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1433542334993137664)

---

**[#🎫︱general-support]** `20:15:37` **josh_clsn** replied to dirvine.:

> *dirvine. said:*
> The network was originally envisaged to be apps running nodes. So everyones computer was a node and they all connected in a large network. Life moved on, mobiles happened, cloud happened and many other things. Anyway we ended up with node runners that means folks not running apps, but just running nodes. 
Some folk running nodes for pure profit will do any amount of harm to others or the network to make a single $0.000001 for themselves. This is the. game we are currently in. It is how it is, people will take everything and leave nothing, given the chance. Not all peopel by any means, but we are the special species that will harm each other cause we can 😉 

However we need to consider this sort of thing more, emissions are a tool to help node runners as we get off the ground, that is takign longer than we wanted, but great progress is being made. 

I think we will be pulled to pieces until we are off the ground, jsut as the bitcoin network would have at teh start, had more folk acted in the extreme greed mode, but the original bitcoin crowd were very different to the new crows in these projects now, that's just how it is. 

I think this is great to report @Dimitar and I hope it's not cost you personally. I don't totally blame that guy, but I am not suprised, the loud accusing voices tend to be the very folks gaming the system as he was. They get a lot of ego boosting from sidelining us and fake reporting other stuff etc. It's also why I get annoyed when we see folk screaming about whales and other folk getting rewards, there is often another reason behind that kind of screaming and shouting.  It's another thing we need to take care off as folk report stuff. They are not always honest 😉  (our community has tended to believe most folk and take them at face value, I am not so inclined to do that any more)

Anyway, it's something to fix for sure, the nodes not behaving for sure need to be cleared out of the network quickly. It is an area where staking does help where bad actors lose stakes. Kinda sad, but true.

I feel guilty campaigning against emissions because I do see the reasons for them too.  
Could the way they are earned perhaps be reevaluated. 

I  feel it is welfare right now not reward for contribution.

Welfare always gets abused.

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433549930974281869)

---


### 💭 Reply to dirvine.

**[#🎫︱general-support]** `20:15:37`

↳ *dirvine. said:*
> The network was originally envisaged to be apps running nodes. So everyones computer was a node and they all connected in a large network. Life moved on, mobiles happened, cloud happened and many other things. Anyway we ended up with node runners that means folks not running apps, but just running nodes. 
Some folk running nodes for pure profit will do any amount of harm to others or the network to make a single $0.000001 for themselves. This is the. game we are currently in. It is how it is, people will take everything and leave nothing, given the chance. Not all peopel by any means, but we are the special species that will harm each other cause we can 😉 

However we need to consider this sort of thing more, emissions are a tool to help node runners as we get off the ground, that is takign longer than we wanted, but great progress is being made. 

I think we will be pulled to pieces until we are off the ground, jsut as the bitcoin network would have at teh start, had more folk acted in the extreme greed mode, but the original bitcoin crowd were very different to the new crows in these projects now, that's just how it is. 

I think this is great to report @Dimitar and I hope it's not cost you personally. I don't totally blame that guy, but I am not suprised, the loud accusing voices tend to be the very folks gaming the system as he was. They get a lot of ego boosting from sidelining us and fake reporting other stuff etc. It's also why I get annoyed when we see folk screaming about whales and other folk getting rewards, there is often another reason behind that kind of screaming and shouting.  It's another thing we need to take care off as folk report stuff. They are not always honest 😉  (our community has tended to believe most folk and take them at face value, I am not so inclined to do that any more)

Anyway, it's something to fix for sure, the nodes not behaving for sure need to be cleared out of the network quickly. It is an area where staking does help where bad actors lose stakes. Kinda sad, but true.

**josh_clsn**: I feel guilty campaigning against emissions because I do see the reasons for them too.  
Could the way they are earned perhaps be reevaluated. 

I  feel it is welfare right now not reward for contribution.

Welfare always gets abused.

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433549930974281869)

---

**[#🌐︱general-chat]** `20:19:29` **aceweb1978** replied to dirvine.:

> *dirvine. said:*
> The gas is actually paid in the autonomi token so you don't need ETH tokens at all?

Oh, that's how it's going to be.... interesting... Thank you very much Dirvine.

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1433550903323000975)

---


### 💭 Reply to dirvine.

**[#🌐︱general-chat]** `20:19:29`

↳ *dirvine. said:*
> The gas is actually paid in the autonomi token so you don't need ETH tokens at all?

**aceweb1978**: Oh, that's how it's going to be.... interesting... Thank you very much Dirvine.

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1433550903323000975)

---

**[#🎫︱general-support]** `20:27:18` **dirvine.** said:

I think we need to consider everything. I Was watching the Solana guy earlier and interesting, bitcoin, eth, solana all went through hell and errors in "getting there". So it's normal, we have faired quite well, but we will get many more scammers and bammers like that dude. I kinda think between the lines we already do have a few in the community and I do see them winding folk up into frenzies and doing so easily as it's always easy to blame "the man" and in our case many times autonomi is seen as "the man" when it suits. 

I am relaxed though as underneath a lot is happeing. i.e. misbehaving nodes are currently handled in many ways, perhaps not all. But the way they are handled is quite unusual and pretty cool in my mind. What will happen is they look normal, their routing tables fill up as normal, but they don't appear in other nodes routing tables.  So they will earn zero or closer to zero than normal nodes. 

There's a few other things happen as well, but we don't speak of them all, all the time. Then of course folk freak out wanting to know everything, but the scammers and bammers are watching, waiting on any small split in the skirt. So we balance. 

Then we work on making nodes as small as possible to run on tiny cheap PC's the counter to that is folk run fekin thousands of them on cloud servers. So we pay for helping the poorer with a repayment fo folk centralising our decentralised network. The balance is hard for sure, every good thing can be mirrored in a bad outcome. 

So we move on learning and finding out more, but like I said watching the solana guy and hearing their story, we are actually quite lucky. But like them we do not put out our 100% complete adn 100% secure never needing to update system, but folk are quick to point out we are not 100% complete in every way and try and lynch us for that too, but that's jsut more nonsense you have to take on board. 

So the trick is, stay cool, stay focussed and keep on moving forward. Realise those who can cause harm, will and those who want you to succeed will have little patience and even less compassion, in many cases and keep going. 

So far we have been very lucky with our wee gang, but some have fallen foul to the holier than though high positioned preacher position, but most have stayed true and kept us moving forward. 

So the key is to remain passionate, but not get emotional and that is hard as passion is likely an emotion 😄 😄 

Balance those apples 😄 😄

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433552869499600927)

---


### 💬 dirvine. posted

**[#🎫︱general-support]** `20:27:18`

**dirvine.**: I think we need to consider everything. I Was watching the Solana guy earlier and interesting, bitcoin, eth, solana all went through hell and errors in "getting there". So it's normal, we have faired quite well, but we will get many more scammers and bammers like that dude. I kinda think between the lines we already do have a few in the community and I do see them winding folk up into frenzies and doing so easily as it's always easy to blame "the man" and in our case many times autonomi is seen as "the man" when it suits. 

I am relaxed though as underneath a lot is happeing. i.e. misbehaving nodes are currently handled in many ways, perhaps not all. But the way they are handled is quite unusual and pretty cool in my mind. What will happen is they look normal, their routing tables fill up as normal, but they don't appear in other nodes routing tables.  So they will earn zero or closer to zero than normal nodes. 

There's a few other things happen as well, but we don't speak of them all, all the time. Then of course folk freak out wanting to know everything, but the scammers and bammers are watching, waiting on any small split in the skirt. So we balance. 

Then we work on making nodes as small as possible to run on tiny cheap PC's the counter to that is folk run fekin thousands of them on cloud servers. So we pay for helping the poorer with a repayment fo folk centralising our decentralised network. The balance is hard for sure, every good thing can be mirrored in a bad outcome. 

So we move on learning and finding out more, but like I said watching the solana guy and hearing their story, we are actually quite lucky. But like them we do not put out our 100% complete adn 100% secure never needing to update system, but folk are quick to point out we are not 100% complete in every way and try and lynch us for that too, but that's jsut more nonsense you have to take on board. 

So the trick is, stay cool, stay focussed and keep on moving forward. Realise those who can cause harm, will and those who want you to succeed will have little patience and even less compassion, in many cases and keep going. 

So far we have been very lucky with our wee gang, but some have fallen foul to the holier than though high positioned preacher position, but most have stayed true and kept us moving forward. 

So the key is to remain passionate, but not get emotional and that is hard as passion is likely an emotion 😄 😄 

Balance those apples 😄 😄

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433552869499600927)

---

**[#🎫︱general-support]** `21:00:21` **dirvine.** said:

Yea I would take everything said by a bammer with a pinch of salt really.  They may be right, they may be wrong, but they tend to be bad sources of info for sure

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433561188096147507)

---


### 💬 dirvine. posted

**[#🎫︱general-support]** `21:00:21`

**dirvine.**: Yea I would take everything said by a bammer with a pinch of salt really.  They may be right, they may be wrong, but they tend to be bad sources of info for sure

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433561188096147507)

---

**[#🎫︱general-support]** `21:06:08` **dirvine.** said:

Now you are feeding scammers more ideas for more scams

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433562642596761654)

---


### 💬 dirvine. posted

**[#🎫︱general-support]** `21:06:08`

**dirvine.**: Now you are feeding scammers more ideas for more scams

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433562642596761654)

---

**[#🎫︱general-support]** `21:10:15` **dirvine.** said:

The days of total open discussion is coming to and end in many ways as we get more folk who would do harm. It's just the world we live in and always will head that way.

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433563680422756412)

---


### 💬 dirvine. posted

**[#🎫︱general-support]** `21:10:15`

**dirvine.**: The days of total open discussion is coming to and end in many ways as we get more folk who would do harm. It's just the world we live in and always will head that way.

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433563680422756412)

---

**[#🎫︱general-support]** `21:16:35` **dirvine.** said:

Of course, that is clear. However if we say 
We are working on a fix for X

Scammer says, Oh wow I never even knew X was an issue and I never knew how to exploit that. So until the fix for X is in place I am gonna scam the fek out of the network using X and get as much as I can. 

Now we are launched and a larger community we simply cannot upfront speak of X. 

It's like the nrmal process of zero day's where folk find the issue and alert the team who fix it then tell folk it's fixed and publish CVE etc. 

I am ready for the many folk saying we should discuss everything up front, but it's not sensible, clever or helpful. I am sure many will see it different, but that is how the industry works and for good reason. Trust in the open community is not a clever way forward with such issues.

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433565272043688127)

---


### 💬 dirvine. posted

**[#🎫︱general-support]** `21:16:35`

**dirvine.**: Of course, that is clear. However if we say 
We are working on a fix for X

Scammer says, Oh wow I never even knew X was an issue and I never knew how to exploit that. So until the fix for X is in place I am gonna scam the fek out of the network using X and get as much as I can. 

Now we are launched and a larger community we simply cannot upfront speak of X. 

It's like the nrmal process of zero day's where folk find the issue and alert the team who fix it then tell folk it's fixed and publish CVE etc. 

I am ready for the many folk saying we should discuss everything up front, but it's not sensible, clever or helpful. I am sure many will see it different, but that is how the industry works and for good reason. Trust in the open community is not a clever way forward with such issues.

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433565272043688127)

---

**[#🎫︱general-support]** `21:16:39` **toivo_toivo** replied to dirvine.:

> *dirvine. said:*
> The days of total open discussion is coming to and end in many ways as we get more folk who would do harm. It's just the world we live in and always will head that way.

How about bug bounties?

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433565290020737055)

---


### 💭 Reply to dirvine.

**[#🎫︱general-support]** `21:16:39`

↳ *dirvine. said:*
> The days of total open discussion is coming to and end in many ways as we get more folk who would do harm. It's just the world we live in and always will head that way.

**toivo_toivo**: How about bug bounties?

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433565290020737055)

---

**[#🎫︱general-support]** `21:18:05` **dirvine.** said:

They don't always do what you think they do. Plus we get 100% plagued by scammers then who claim to have found an issue we need to pay for before they tell us what it is and so on. 

Of course many fok will also say this is wrong too 😉

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433565649560666234)

---


### 💬 dirvine. posted

**[#🎫︱general-support]** `21:18:05`

**dirvine.**: They don't always do what you think they do. Plus we get 100% plagued by scammers then who claim to have found an issue we need to pay for before they tell us what it is and so on. 

Of course many fok will also say this is wrong too 😉

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433565649560666234)

---

**[#🎫︱general-support]** `21:20:54` **josh_clsn** replied to dirvine.:

> *dirvine. said:*
> They don't always do what you think they do. Plus we get 100% plagued by scammers then who claim to have found an issue we need to pay for before they tell us what it is and so on. 

Of course many fok will also say this is wrong too 😉

If you get to choose your next life will it be librarian instead? 😆

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433566359849275415)

---


### 💭 Reply to dirvine.

**[#🎫︱general-support]** `21:20:54`

↳ *dirvine. said:*
> They don't always do what you think they do. Plus we get 100% plagued by scammers then who claim to have found an issue we need to pay for before they tell us what it is and so on. 

Of course many fok will also say this is wrong too 😉

**josh_clsn**: If you get to choose your next life will it be librarian instead? 😆

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433566359849275415)

---

**[#🎫︱general-support]** `21:21:44` **dirvine.** said:

I am salivating at the robots coming with their AI brains 😄 😄 I will make peace with them and love learning from them

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433566568838598667)

---


### 💬 dirvine. posted

**[#🎫︱general-support]** `21:21:44`

**dirvine.**: I am salivating at the robots coming with their AI brains 😄 😄 I will make peace with them and love learning from them

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433566568838598667)

---

**[#🎫︱general-support]** `21:23:25` **dirvine.** said:

We would need hundreds of escrows per week in that case. It all sounds so easy, but seriously folk have zero idea of the amount of scam emails and claims and so on.
Reality is so different from what folk think

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433566994711449671)

---


### 💬 dirvine. posted

**[#🎫︱general-support]** `21:23:25`

**dirvine.**: We would need hundreds of escrows per week in that case. It all sounds so easy, but seriously folk have zero idea of the amount of scam emails and claims and so on.
Reality is so different from what folk think

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433566994711449671)

---

**[#🎫︱general-support]** `21:26:00` **dirvine.** said:

Here is how it goes, 
I have found a serious bug, pay XX to this BTC or Zcash address and I will fix it. I will not tell you who I am, I will use a VPN and ......

On an on that crap goes, you cannto work with the levels fo scam that are out there. It's seriously not what you think it is.

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433567644866580500)

---


### 💬 dirvine. posted

**[#🎫︱general-support]** `21:26:00`

**dirvine.**: Here is how it goes, 
I have found a serious bug, pay XX to this BTC or Zcash address and I will fix it. I will not tell you who I am, I will use a VPN and ......

On an on that crap goes, you cannto work with the levels fo scam that are out there. It's seriously not what you think it is.

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433567644866580500)

---

**[#🎫︱general-support]** `21:27:57` **dirvine.** said:

It's one way of making the point clear for everyone.

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433568133322510477)

---


### 💬 dirvine. posted

**[#🎫︱general-support]** `21:27:57`

**dirvine.**: It's one way of making the point clear for everyone.

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433568133322510477)

---

**[#🎫︱general-support]** `23:08:38` **27poke** replied to dirvine.:

> *dirvine. said:*
> The network was originally envisaged to be apps running nodes. So everyones computer was a node and they all connected in a large network. Life moved on, mobiles happened, cloud happened and many other things. Anyway we ended up with node runners that means folks not running apps, but just running nodes. 
Some folk running nodes for pure profit will do any amount of harm to others or the network to make a single $0.000001 for themselves. This is the. game we are currently in. It is how it is, people will take everything and leave nothing, given the chance. Not all peopel by any means, but we are the special species that will harm each other cause we can 😉 

However we need to consider this sort of thing more, emissions are a tool to help node runners as we get off the ground, that is takign longer than we wanted, but great progress is being made. 

I think we will be pulled to pieces until we are off the ground, jsut as the bitcoin network would have at teh start, had more folk acted in the extreme greed mode, but the original bitcoin crowd were very different to the new crows in these projects now, that's just how it is. 

I think this is great to report @Dimitar and I hope it's not cost you personally. I don't totally blame that guy, but I am not suprised, the loud accusing voices tend to be the very folks gaming the system as he was. They get a lot of ego boosting from sidelining us and fake reporting other stuff etc. It's also why I get annoyed when we see folk screaming about whales and other folk getting rewards, there is often another reason behind that kind of screaming and shouting.  It's another thing we need to take care off as folk report stuff. They are not always honest 😉  (our community has tended to believe most folk and take them at face value, I am not so inclined to do that any more)

Anyway, it's something to fix for sure, the nodes not behaving for sure need to be cleared out of the network quickly. It is an area where staking does help where bad actors lose stakes. Kinda sad, but true.

"The network was originally envisaged to be apps running nodes. So everyones computer was a node and they all connected in a large network. Life moved on, mobiles happened, cloud happened and many other things. Anyway we ended up with node runners that means folks not running apps, but just running nodes. "                    Everything that can be exploited will be exploited, everyone should know that, as it has probably been known since at least 2000 years. Instead a few people believed in fairytales that apps can run nodes, people with phones can run nodes a few hours. The network NEEDS TO BE DEFENDED AT ALL COST, ABOVE ALL, AT ALL TIMES. Evertyhing that can be exploited will be exploited, even if the consequences is the death of the network. Hope this becomes a wake up call for all in charge, not pointing fingers but the naivity needs to be gone, yesterday. @Bux @dirvine No more of the fairytale BS of running nodes only a few hours, nodes needs to be rewarded for keeping data over time, the longer time the higher the rewards, no more talk about running nodes a few hours on phones or other crap.

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433593472677581002)

---


### 💭 Reply to dirvine.

**[#🎫︱general-support]** `23:08:38`

↳ *dirvine. said:*
> The network was originally envisaged to be apps running nodes. So everyones computer was a node and they all connected in a large network. Life moved on, mobiles happened, cloud happened and many other things. Anyway we ended up with node runners that means folks not running apps, but just running nodes. 
Some folk running nodes for pure profit will do any amount of harm to others or the network to make a single $0.000001 for themselves. This is the. game we are currently in. It is how it is, people will take everything and leave nothing, given the chance. Not all peopel by any means, but we are the special species that will harm each other cause we can 😉 

However we need to consider this sort of thing more, emissions are a tool to help node runners as we get off the ground, that is takign longer than we wanted, but great progress is being made. 

I think we will be pulled to pieces until we are off the ground, jsut as the bitcoin network would have at teh start, had more folk acted in the extreme greed mode, but the original bitcoin crowd were very different to the new crows in these projects now, that's just how it is. 

I think this is great to report @Dimitar and I hope it's not cost you personally. I don't totally blame that guy, but I am not suprised, the loud accusing voices tend to be the very folks gaming the system as he was. They get a lot of ego boosting from sidelining us and fake reporting other stuff etc. It's also why I get annoyed when we see folk screaming about whales and other folk getting rewards, there is often another reason behind that kind of screaming and shouting.  It's another thing we need to take care off as folk report stuff. They are not always honest 😉  (our community has tended to believe most folk and take them at face value, I am not so inclined to do that any more)

Anyway, it's something to fix for sure, the nodes not behaving for sure need to be cleared out of the network quickly. It is an area where staking does help where bad actors lose stakes. Kinda sad, but true.

**27poke**: "The network was originally envisaged to be apps running nodes. So everyones computer was a node and they all connected in a large network. Life moved on, mobiles happened, cloud happened and many other things. Anyway we ended up with node runners that means folks not running apps, but just running nodes. "                    Everything that can be exploited will be exploited, everyone should know that, as it has probably been known since at least 2000 years. Instead a few people believed in fairytales that apps can run nodes, people with phones can run nodes a few hours. The network NEEDS TO BE DEFENDED AT ALL COST, ABOVE ALL, AT ALL TIMES. Evertyhing that can be exploited will be exploited, even if the consequences is the death of the network. Hope this becomes a wake up call for all in charge, not pointing fingers but the naivity needs to be gone, yesterday. @Bux @dirvine No more of the fairytale BS of running nodes only a few hours, nodes needs to be rewarded for keeping data over time, the longer time the higher the rewards, no more talk about running nodes a few hours on phones or other crap.

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433593472677581002)

---


## Friday, 2025-10-31

**[#🎫︱general-support]** `10:16:50` **dirvine.** said:

What point do you think you are making here?

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433761630432530515)

---


### 💬 dirvine. posted

**[#🎫︱general-support]** `10:16:50`

**dirvine.**: What point do you think you are making here?

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433761630432530515)

---

**[#🎫︱general-support]** `10:28:33` **dimitarsafenetworkbulgaria** replied to dirvine.:

> *dirvine. said:*
> What point do you think you are making here?

I doubt he understands the problem. @27poke  everything is fine, just a hole needs to be closed, we should be grateful to people like the Fake IT Guy, ready to try to break the network for pennies. When the network costs billions there will be real professionals trying to break it.

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433764578122268784)

---


### 💭 Reply to dirvine.

**[#🎫︱general-support]** `10:28:33`

↳ *dirvine. said:*
> What point do you think you are making here?

**dimitarsafenetworkbulgaria**: I doubt he understands the problem. @27poke  everything is fine, just a hole needs to be closed, we should be grateful to people like the Fake IT Guy, ready to try to break the network for pennies. When the network costs billions there will be real professionals trying to break it.

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1433764578122268784)

---

