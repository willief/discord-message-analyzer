# dirvine. Weekly Digest

*Week of 2026-02-22 to 2026-03-08*

*Generated: 2026-03-08 23:25:32 UTC*

**Messages this week: 130**

This digest contains dirvine.'s recent posts and replies to their messages.

---


## Sunday, 2026-02-22

**[#🎙︱discussion-topics]** `13:10:25` **dirvine.** said:

I kinda have not aimed at data centers and working well for huge corporate networks 😉 Sorta my thing. I am sure many folk will lecture me and remind me though. It seems constant

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1475117529432330445)

---

**[#🎙︱discussion-topics]** `13:11:49` **dirvine.** said:

Now we are OSS I think folk neeed to fork and do their own networks, it will only make us all better.

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1475117882798112900)

---

**[#🎙︱discussion-topics]** `20:55:05` **southside_the_magnificent** replied to dirvine.:

> *dirvine. said:*
> Now we are OSS I think folk neeed to fork and do their own networks, it will only make us all better... [truncated]

Admit it  ---   @Dimitar paid you to say that 🙂

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1475234469182046482)

---

**[#🎙︱discussion-topics]** `21:47:06` **janeytheterrible** replied to dirvine.:

> *dirvine. said:*
> I kinda have not aimed at data centers and working well for huge corporate networks 😉 Sorta my thing... [truncated]

Here is an exchange where testing showed they had to reduce the window size due to frame blocking  to get better results.  Note a frame is a window_sized data block.  When set to 10MB Max (initial) then router buffers overflow with just a few chunks from the one machine (multiple nodes here) https://www.mail-archive.com/quic%40ietf.org/msg03789.html

And here, while only one QUIC on a machine (we have one for each node, so multiply the issues and therein is the problems of router buffer overflow)  https://docs.google.com/document/d/1F2YfdDXKpy20WVKJueEf4abn_LVZHhMUMS5gX6Pgjl4/mobilebasic

Even Google sets their default initial window sizes to very small values
```
Default values

Google’s servers default to enable auto-tuning for  receive buffers, with the following initial window size settings:

   CFCW: 49152 // 48 KB
  SFCW: 32768 // 32 KB
```

And the QUIC documents says to set that value for your application.  Remember with multiple nodes (independent QUICs) then buffer size in the potato ISP routers are a constraint that QUIC QUIC does not know about and has to learn for each new connection (chunk/node)
```
There is a maximum flow control receive window size which is chosen independently by each endpoint. An endpoint should base this decision on available resources - if you are not constrained by memory then set a large window of 100 Mb for example, whereas a busy server may set a window of 64 Kb. ```

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1475247557738234017)

---


## Monday, 2026-02-23

**[#🎙︱discussion-topics]** `15:00:10` **dirvine.** said:

What we do now so folk know. 
setup several computers all over the world and in local networks. 
Run them all with AI, full logging on (asyn) 
Have the AI monitor logs, look for inconsistencies 

Do deep research on each finding, involve many AI's in deep research max thinking mode 
Work with them, agree a plan 

Run test again, both tests fully benchmarked. 

Not notions or idea or suggestions, real world testing of ALL of the tweaks we can make

It is super super easy to convince ourselves of a single parameter like this discussion and just doggedly go after that one param, never to ask why? It may be correct @neo it may well be, but it's one thing of thousands of other things that all must be considered together.  Otherwise there would be a 
- Data center 
- Home user 
Setting and we would be done with it. 

It's seriously not simple and it's absolutely 100% certain not a single param change we need to consider.

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1475507537309859971)

---

**[#🎙︱discussion-topics]** `17:02:17` **dirvine.** said:

We did change it in the network, we rolled it out, the network went batshXt, we reversed 
it back out of the network. We are gonna end up embarrassing folk here btw, it's not good, the team listened, the team tried, we need to hear what is being said. 

I cannot stress enough how poking any single thing like this is beyond insane, we tried, it screwed up the network. I am sure we could change it again and incur even more data loss. 

Seriously guys, this is beyond mental, does anyone actually know what this single setting actually does and then does anyone know how it relates to all other setting in the network? 

How many times do we need to just change stuff like this, just cause .... ? 

This is an auto negotiated setting BTW, but I don't think that even matters in the frenzy

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1475538268605911201)

---

**[#🎙︱discussion-topics]** `17:08:41` **dirvine.** said:

sigh

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1475539881206878480)

---

**[#🎙︱discussion-topics]** `17:10:04` **dirvine.** said:

Do you mean do it again? How many times do you want us to actually do it?

I honestly don't think people listen at all or read what's being said. It's been said gently for a while by @Shu and others. The amount of research into this thing would make your eyes water. To hear people just going "single setting, single setting, single setting" on top of "native token, native token, native token," it's seriously bad quality behavior

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1475540229258612797)

---

**[#🎙︱discussion-topics]** `17:11:44` **dirvine.** said:

Who would ever do open source? the rewards are near zero, the pain is near 100%, and the constant, utter, belligerent lecturing is beyond belief

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1475540645589553266)

---

**[#🎙︱discussion-topics]** `17:19:56` **dirvine.** said:

IT HAS BEEN TRIED. IT BROKE THE NETWORK 
IT HAS BEEN TRIED. IT BROKE THE NETWORK 
IT HAS BEEN TRIED. IT BROKE THE NETWORK

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1475542712139645050)

---

**[#🎙︱discussion-topics]** `17:21:05` **dirvine.** said:

I sorry, Massa. I'm very sorry. I should have made it clearer. I'm really sorry, Massa. Please don't whip me again.

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1475542999097282671)

---

**[#🎙︱discussion-topics]** `17:22:45` **dirvine.** said:

There was some point when I was ill that we changed from a community that could collaborate on an equal footing to a bunch of people (not that many, but a bunch) who started just lecturing and demanding. 

I don't really know how that happened or where it came from. I wonder if these people walk down the street and tell other people that they're wearing their clothes wrong or they're walking the wrong way, but something changed. People started lecturing instead of listening, just continually going on about the same thing over and over again. 

It's a weird thing to watch, and it's an even weirder thing to try and understand.

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1475543420675035157)

---

**[#🎙︱discussion-topics]** `17:23:45` **dirvine.** said:

Well, judging by this conversation, yes

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1475543670353694862)

---


## Tuesday, 2026-02-24

**[#🎙︱discussion-topics]** `06:25:02` **dimitarsafenetworkbulgaria** replied to dirvine.:

> *dirvine. said:*
> There was some point when I was ill that we changed from a community that could collaborate on an eq... [truncated]

This is normal and expected behavior. We have a group of people who want to help, but because they don't have a complete picture of the whole picture, they think that the color of the paint determines how stable the ship is, and they really want the color to be just right so that the ship can be stable. No matter how much the engineer explains that color doesn't affect stability, people feel that it does because color is what they see. When it comes to such feelings, it's a waste of time to discuss them, but to keep the community strong, it's good to pay attention to feelings. For this purpose, I have an AI persona that I use to talk acknowledging people's feelings and at the same time not wasting my time.

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1475740288067698729)

---

**[#🎙︱discussion-topics]** `09:58:37` **dirvine.** said:

Yeah, for sure. There's an awful lot of parameters to take into consideration, and there's a lot of pretty good information so far

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1475794038128115786)

---

**[#🎙︱discussion-topics]** `10:02:00` **dirvine.** said:

To me, we need to get to a position where nodes are adaptive and can actually self-configure. There is no real "golden set" of configurations; networking is a nightmare, which is why there are so many settings, yet none of them suit everybody. While advanced users in the community might not mind tweaking things, that isn't the goal here. The goal should be "click, install, and work," so nodes must become much more adaptive.

Where we do have issues—which QUIC tries to address—is when you need negotiated protocol settings. There are quite a lot of them, and that's another angle to consider. It is a bit like a spaceship: if someone suggests taking one part out, it feels dangerous.

I believe the network will eventually evolve into an adaptive mechanism where nodes self-configure over time. That is the ultimate goal, because otherwise, networking is simply too hard. People will always want the specific configuration they think suits them, but the amount of parameters is staggering. Since personal networks change constantly, leaning toward adaptive nodes is a key component.

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1475794890028748801)

---

**[#🎙︱discussion-topics]** `10:12:56` **dirvine.** said:

I feel we should move away from this "node runner" concept, which is probably alarming for some people. The key really is that these nodes should run on everyone's computer without needing lots of configuration, and they certainly should not be affecting the computer or the network adversely.

Basically, they should be an almost invisible component of the applications people are running. That invisible component should allow them to share the resources of their machine with people who have fewer resources, who may need to use tokens to store data instead of buying new machines.

The winning component is that even if your machine blows up or catches fire, your data is still okay if you are storing it on the network.

I feel like we are missing the target with the amount of work being done for node runners. When it becomes a "node runner" conversation, it all becomes about money:
1. How much am I getting?
2. How much can I earn?
3. How many of these things can I get to make more money?

While that is fascinating in some ways, I think it means we've missed the target slightly. It should be about secure access for everyone. Everyone should be able to participate fully in the network, and the "node runner" thing has just never felt very good to me.

It has been great to test nodes, but that is not the direction. The direction is that these nodes should be really beneficial to everybody. People should have a clear understanding that their data is secure—not only from people reading it, but from the raw hardware melting down.

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1475797642482159636)

---

**[#🎙︱discussion-topics]** `10:41:49` **27poke** replied to dirvine.:

> *dirvine. said:*
> I feel we should move away from this "node runner" concept, which is probably alarming for some peop... [truncated]

From my own experience people don't like to have their computers on 24/7 and nodes tend to love a life were they are always on and don't cause churn across the network.

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1475804907385655296)

---

**[#🎙︱discussion-topics]** `10:44:56` **dirvine.** said:

This is another advantage of AI. We're moving into a different world where these things will be on 24/7. But even without it being on 24/7, if the network is adaptive enough, that shouldn't matter.

Autonomi 2, for instance, has a neural network and LSTM (Long Short-Term Memory), which allows it to:
1. Predict when particular computers are off and on
2. Work out churn prediction

This is what I mean about being adaptive: the network has to be adaptive, and not only in the networking core, if you know what I mean.

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1475805691825492048)

---

**[#🎙︱discussion-topics]** `11:10:13` **27poke** replied to dirvine.:

> *dirvine. said:*
> This is another advantage of AI. We're moving into a different world where these things will be on 2... [truncated]

The theory and research sounds very exciting, it seems difficult to know how it will work in the real world right now.

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1475812056107188327)

---

**[#🎙︱discussion-topics]** `13:18:08` **b_dazz** replied to dirvine.:

> *dirvine. said:*
> I feel we should move away from this "node runner" concept, which is probably alarming for some peop... [truncated]

In order to level the playing field and provide earnings potential to everyone there should be some kind of lottery component to the network, a veritable golden ant that could be won periodically by anyone, including mobile users. The probability of winning this golden ant should not be a function of how many nodes are being run. Otherwise, there will always be a race for resource superiority.

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1475844246069182586)

---

**[#🎙︱discussion-topics]** `13:19:50` **dirvine.** said:

I am moving forward, securing the vision, I will not be stopped, we all should be looking forward. I lead with respect, but after many many times repeating the same thing, I will push back. Always. 

When asked to do X and I say we did X and then continually being asked to do X and continually saying we have done X is howling at the moon territory. It's useless and I have too much to do. 

Moving at speed means not going slow, so I can give my opinion and receive opinion, but I cannot get stuck in dogged persistant demands are a form of slavery. We should be much better than that.

So we move forward or stop and pontificate ourselves to a standstill. 

Debate is great, opinions are superb, dogged persistence is not acceptable to me. 

Our time is right now and we need to get a shift on.

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1475844676018765866)

---

**[#🎙︱discussion-topics]** `13:20:08` **dirvine.** said:

That is the way

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1475844749947699210)

---

**[#🎙︱discussion-topics]** `14:07:48` **traktion0_20257** replied to dirvine.:

> *dirvine. said:*
> I feel we should move away from this "node runner" concept, which is probably alarming for some peop... [truncated]

Personally, I think all flavours of node running should be tolerated. I suspect there will always be a mix of flavours too, unless there is code to be hostile against certain uses (which may be tough in itself).

For example, I may want a 'light' app which doesn't do node duties. A simple, thin client app. Likewise, I may want a 'heavy' app, which runs a node too, as it is long running and I don't want to think about node setup. I may want to run the 'light' version on my phone, but then run some nodes on spare, old, hardware at home to earn tokens to fund the 'light' app operation.

So, it feels like a choice thing. Maybe the default should be the simplest, but power users will always tinker. There may also be a question of long running nodes, which need 24/7 access, to avoid heavy churn, improve network performance, etc. It feels like there nedes to be a balance across these different needs of users and the network.

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1475856747884445840)

---

**[#🎙︱discussion-topics]** `15:33:09` **dirvine.** said:

Without a doubt, all you say is 100% agreed in my head. What I am saying is not to prevent any use, but to shift focus from power users (node runners) to ordinary people.

It's code, folk can and will do what they want, but we should not target power users and instead make it super super simple for ordinary people to be part of the eco-system. 

If you look on here or the community forum there is so much, how many nodes can I run, how much do I get and all that kind of thing. While it's superb folk run nodes to help (most of the old community do just that), the community that is building has an ever growing presence of folk who want to earn, ignore the wee lassie in Africa, just show me the money. 

So the shift from community for the good can shift to community for the money, bitcoin did that and we are heading that way. So the focus, the true grit of this has to be value for the wider audience. 

When true decentralisation and value creation and flow becomes an obvious incentive to simply extract cash, that is what will happen and we risk that very thing. 

Ultimately the good folk don't see it, they cannot notice it, but this is what I feel we are heading towards. 

So absolutely there wil always be all ways of using this, but if we continue to focus on node runners and token extraction alone we failed. We must provide value for all, then the ANT token value rises and we all win. Not a select few who managed to grab theirs and run.

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1475878224868147447)

---

**[#🎙︱discussion-topics]** `16:44:14` **mightyfool0689** replied to dirvine.:

> *dirvine. said:*
> I am moving forward, securing the vision, I will not be stopped, we all should be looking forward. I... [truncated]

I hope you realize that I’m saying this from a place of respect as well and wouldn’t say it if I didn’t have the networks best interest at heart. I do think that sometimes you can lash out a bit at people because they ask something for the first, maybe second time, because you’ve heard the question/remark/advice a thousand times already. And while I understand from your point of view that that 1000th question justifies pushing back, but I think you’re pushing back at the wrong people.

You guys choose to not always reply in depth to community concerns, and I have the greatest respect for that decision as it would otherwise simply consume too much of your and the team’s time. But I would recommend that you try to realize that that time saving sometimes results in people asking the same question multiple times. Not because they demand things, but I think most of the times it’s because they simply were not aware it’s been asked before or because they feel it’s important and they’re not sure if the team is aware. The few cases where it really is demanding aside.

To emphasize this further, the discussion of yesterday about Neo’s window size. I had absolutely no idea it’s been tried before and it broke the network. And I’m literally around 24/7 on Discord and the Forum reading everything. I think it’s good that these concerns are raised and I also appreciate you taking the time to discuss that somewhat in depth.

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1475896116443615323)

---

**[#🎙︱discussion-topics]** `17:05:33` **dirvine.** said:

sigh

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1475901476948934720)

---

**[#🎙︱discussion-topics]** `21:11:58` **dirvine.** said:

Here's some commits for folk to dive into, there's tones more

There goes another 45 minutes of wasted time. 

I hope this pleases folk, satisfies others and likely it tells everyone absolutely he haw!! 


```
 ### Commits where max_stream_data (or equivalent QUIC receive window behavior) changed

 - 1fbab5c56 (2025-01-07)
 File: ant-networking/src/transport.rs
 Change: Added ANT_MAX_STREAM_DATA env override and set:
 quic_config.max_stream_data = <env parsed u32>.
 - 473b92019 (2025-06-12)
 File move: ant-networking/src/transport.rs → ant-node/src/networking/transport.rs
 Change: Code moved (behavior preserved).
 - 7ec45124a (2025-11-14)
 File: autonomi/src/networking/driver/mod.rs
 Change: Client set hardcoded:
 quic_config.max_stream_data = 1024 * 1024 (1MB).
 - 20977e22e (2025-11-15)
 File: autonomi/src/networking/driver/mod.rs
 Change: Client switched to env override again with default 1MB:
 ANT_MAX_STREAM_DATA + .unwrap_or(1024 * 1024).
 - def2b2cb2 (2025-11-17)
 File: ant-node/src/networking/transport.rs
 Change: Node removed env override and hardcoded:
 quic_config.max_stream_data = 1024 * 1024.
```

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1475963492673782001)

---

**[#🎙︱discussion-topics]** `21:25:55` **dirvine.** said:

Anybody interested can look at what I told Rob at the time https://forum.autonomi.community/t/discussion-on-low-level-data-flow-and-home-networks-found-solution-to-allow-4mb-max-chunk-size-as-smooth-as-1-2-mb-its-a-setting-in-quic/40540/13

For clarity at that time, I could not eat, speak or open my mouth 

So I really think I will take the lectures lightly about how I don't care. I could barely type back then. Never mind get into long drawn out discussions and explanations, but the guys did try. 

We either want this thing done or we don't. I am pretty motivated to actually get it done.

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1475967003733918029)

---

**[#🎙︱discussion-topics]** `21:34:46` **janeytheterrible** replied to dirvine.:

> *dirvine. said:*
> This is another advantage of AI. We're moving into a different world where these things will be on 2... [truncated]

FYI in case you had not seen this in QUIC before

Did you know about QUIC doing some of this work taking in suggestions for adapting.  You could have your adaptive system do its magic of analysing conditions and so on and that help QUIC do its job.

_"I believe the network will eventually evolve into an adaptive mechanism where nodes self-configure over time. "_

One of the things that QUIC allows it to be told, amongst others, is a initial_window_size which helps.  Since QUIC on a home system will always see a 1Gbps network connection, never blocked since its UDP, it needs helps to not cause buffer overflows in the router.  8MB buffers are a pain.

So setting initial_window_size based on your adaptive system will allow each node and its copy of QUIC to be helped.  I would say the response time to the first messages to the receiving node can set a base line for lag to that receiving node and then your adaptive system can monitor retry requests to be able to tailor things.

Its one of the settings for this purpose.

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1475969230259224636)

---

**[#🎙︱discussion-topics]** `21:38:39` **dirvine.** said:

Yes, seriously man I have devoured the IETF QUIC specs and p2p updates (not yet in place) as well as the seemans specs on native nat traversal MASQUE relays and more. I way way way in those weeds 😉 

This setting here is one in a sea of things to consider 😉

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1475970207901159567)

---


## Wednesday, 2026-02-25

**[#🎙︱discussion-topics]** `09:59:37` **dirvine.** said:

There is an issue in this conversation. There were links to forum discussions and papers on the topic, Autonomi 1 has commits and documentation on the topic, and Autonomi 2 has huge amounts of documentation. 

How do you handle that? Are you supposed to copy all of these documents into every reply, or do people go and read them? We have posted links to docs, and there are humongous amounts of information available. There was lots of information given in the conversation (including saying countless times we tried) , and I think that is where the problem is. 

Humans want something delivered:
1. Exactly how they want it delivered
2. When they want it delivered
3. At exactly the right time and place that they want it delivered

This is why I have hope for AI. Anybody in this conversation could have pointed their AI to the code, to the IETF specifications, and to the forum discussions to get a complete picture of what is actually happening. But for some reason, humans want other humans to do that job for them, and that is one thing I am really looking forward to with AI.

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1476156675550613505)

---

**[#🎙︱discussion-topics]** `10:01:36` **dirvine.** said:

You can also go to the libPTP forum and see why they set it at that, what testing they did to establish that particular setting, and why that setting was chosen after a considerable amount of engineering time spent on it with another engineering team (nothing to do with Autonomi).

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1476157176589320303)

---

**[#🎙︱discussion-topics]** `10:02:04` **dirvine.** said:

You'll also see there MaidSafe engineers questioning it and trying to figure out any more information that they could get on it

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1476157293170004089)

---

**[#🎙︱discussion-topics]** `10:41:23` **dirvine.** said:

I 100% do not indicate debate, discussion and opinion is not valid, that is manipulation!!!! How can you even hint that is the case on a very forum I am discussing on, it's wild wild bending of the truth. 

However constant demands for change with no real evidence is stupid, full stop, Repeated calling for something for OVER A YEAR is not helpful, particularly when there is a ton of work and evidence being ignored. (same for native token chants) 

So do not manipulate what I am saying in that fashion, It's unbecoming and 100% why there is angry discourse. Telling folk how and what to think is entirely wrong. 

Yes, we are busy, YES WE DO TAKE TIME TO COMMUNICATE, and yes we care.

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1476167189575893107)

---

**[#🎙︱discussion-topics]** `11:14:09` **dirvine.** said:

You're taking a very high ground there. I know you always like the last word, and you do like the high ground. Don't take the high ground with me. Don't take it with anybody

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1476175432134164651)

---

**[#🎙︱discussion-topics]** `20:13:32` **dirvine.** said:

Don't worry about me, I am very focussed, motivated and working at 10X normal pace 😉

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1476311172763353100)

---


## Thursday, 2026-02-26

**[#🎙︱discussion-topics]** `07:33:01` **fte3680001** replied to dirvine.:

> *dirvine. said:*
> Without a doubt, all you say is 100% agreed in my head. What I am saying is not to prevent any use, ... [truncated]

"When true decentralisation and value creation and flow becomes an obvious incentive to simply extract cash, that is what will happen and we risk that very thing. "

Maybe the message on https://autonomi.com/node should be changed a bit.
"Contribute your spare resources and get paid. " - This creates wrong expectations and attracts the wrong people.

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1476482171945353319)

---

**[#🎙︱discussion-topics]** `09:46:17` **dirvine.** said:

I don't know that is correct actually. We do not have internal debates, but we do discuss a lot. 

My take and I believe others is this. 

The network can have tremendous value. 

That value translates into paying those who provide resource FROM those who require resource.

Now here is the key, an economy only works when there are inputs and outputs. Value offered and value paid for if that makes sense. 

However focusing on node runners means we focus on EXTRACTION but no VALUE provision. 

i.e. we cannot have extraction with no provision. 

Then we add in the decentralised component. So share value widely and offer value widely.  

This means we are looking for ways to allow value provision to balance value extraction. 

Where node runners come in (in my eyes) is centralising as much extraction as possible to benefit the few. 

The very thing we wish to avoid. 

So we can get security, privacy etc. for people, but that key and critical component of value extraction is an issue. The whole idea was your computer runs, the node runs, it earns you some cash, not enough to profit wildly but enough to pay for your resources, disk, cpu electricity etc. 

What happens though is folk say, theres a £0.0001 profit here, if I run a million of these I can extract an uneven amount from this network. That upsets the balance. 

This is how I would frame it. 

We all want value, but I am super keen the value is distributed and not concentrated and especially so at the cost of centralising a decentralised network.

People always think I hate money, I do not hate it, I think value is brilliant, I love it, but I don't think about it in any shallow way.

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1476515708908212234)

---

**[#🎙︱discussion-topics]** `09:59:24` **dirvine.** said:

Getting to scale and how are important. Very important. Relying on good will will not do it. We need to be smarter and not rely on early adopters not centralising. 

The early adopters will WIN much more by letting the network grow and their share/tokens appreciate. Many though will want to grab as many tokens as possible, even at the cost of not letting it really grown. 

Short term human greed outperforms long term gains and good for all. It's just how it is, no right or wrong, but we cannot ignore it. 

So smarter we have to be 😄

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1476519012333785178)

---

**[#🎙︱discussion-topics]** `14:22:17` **b_dazz** replied to dirvine.:

> *dirvine. said:*
> I don't know that is correct actually. We do not have internal debates, but we do discuss a lot. 

M... [truncated]

All over the world there is a growing conflict between data center operators and residents opposed to the noise and economic shifts related to the centers. Might this be an opportunity that Autonomi can take advantage of, that is, providing millions of distributed data centers around the world run by individuals without the noise, electrical usage and economic drain that currently exists? Couldn’t this be the inherent “value” of the network that is mostly missing right now?

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1476585166511149170)

---

**[#🌐︱general-chat]** `15:54:55` **dirvine.** said:

Yes, it's great

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1476608481246318663)

---

**[#🌐︱general-chat]** `16:28:06` **dirvine.** said:

ant-quic is already wired for this 😉

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1476616829266034841)

---

**[#🌐︱general-chat]** `16:58:06` **dirvine.** said:

Autonomi 2.0 is almost a different thing, but it won't be just nodes and clients. It's going to be significantly more than that. Many parts of it will use the internet but will also continue to work when the internet's not there, using other methods very like Reticulum

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1476624381080899584)

---

**[#🌐︱general-chat]** `18:53:31` **dirvine.** said:

It is interesting, but be aware it's not a general networking thing yet. It's pretty much still radio-based and meant for catastrophic network failure or whatever. So, it's not just something to run nodes on at this moment in time.

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1476653425658826894)

---

**[#🌐︱general-chat]** `20:17:32` **phraxtzu** replied to dirvine.:

> *dirvine. said:*
> It is interesting, but be aware it's not a general networking thing yet. It's pretty much still radi... [truncated]

That makes sense. I guess my mind goes to catastrophic failure type situations easily because I've spent most of my life off grid or in really remote areas... haha

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1476674570793648159)

---


## Friday, 2026-02-27

**[#🎫︱general-support]** `07:42:10` **dirvine.** said:

Not yet, but things are gonna be different for sure. Hopefully community will be much more engaged and their jobs made simpler too

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1476846863658258593)

---

**[#🎫︱general-support]** `08:57:20` **janeytheterrible** replied to dirvine.:

> *dirvine. said:*
> Not yet, but things are gonna be different for sure. Hopefully community will be much more engaged a... [truncated]

One thing that would help me greatly is if its possible to have some testnets without any requirement to pay for uploads.  Test tokens can be a hinderance in some cases and make it harder for testing

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1476865780212695225)

---

**[#🎫︱general-support]** `09:06:09` **dirvine.** said:

Yeah, me too. It's a tricky one because when you're not doing the payments, you get a totally different experience.

The testnets now are more tricky because we've got geo-blocking (IP-type blocking), so you can't run them all on DigitalOcean or from the same geography. It's all for security, so there's a lot of tricky stuff we've got to get around.

But yeah, I think I feel the same as you, Rob. The payments add so much to the flow; it's very difficult to switch them off and on in the code.

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1476867995749060699)

---

**[#🎫︱general-support]** `09:24:25` **dirvine.** said:

Exactly, these are all the things that we're working on, but there are answers to those kind of things

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1476872595981860948)

---

**[#🎫︱general-support]** `11:18:45` **dirvine.** said:

These are questions for your AI 😉

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1476901366969663553)

---

**[#🎫︱general-support]** `17:20:06` **dirvine.** said:

It's only about keeping data distributed. Later, we may actually use masque relays so that we don't have a clue—or the network doesn't have a clue—where the uploader is situated, so it will be truly decentralized.

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1476992305180315810)

---

**[#🎫︱general-support]** `20:03:29` **ucanteneke** replied to dirvine.:

> *dirvine. said:*
> These are questions for your AI 😉

not asking a question, just stating something 😄

[View in Discord](https://discord.com/channels/1209059621319221268/1247881515107483759/1477033419580903607)

---


## Saturday, 2026-02-28

**[#🎙︱discussion-topics]** `11:04:08` **dirvine.** said:

No, not yet, I think start would be great and something to build on. I have some ideas etc. but nothing fixed. To be honest, with AI coming and its ability to de-anonymize, I think things could change quickly. Whether it is good or bad that everybody is public, there are arguments to and for.

In the past week or so, I have been looking deep at the anonymity question and the actual fact of security. In terms of if the economy changes, would there be a need to steal money from other people? If you take the need to steal money away (or stealing money being useful), and anonymity is gone, then you have to ask yourself: what data are we trying to secure and for what purpose?

It is quite deep. I don't have any answers, and I'm sure people will go completely crazy even because I'm thinking about it, but I think it's something we need to consider.

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1477260075616702464)

---

**[#🎙︱discussion-topics]** `11:35:56` **dirvine.** said:

Fine to clean up for now I think. If it's an issue then do clean up, if it's easy to leave then leave. We will get some info from this but we don't depend on it.

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1477268079359688818)

---

**[#🎙︱discussion-topics]** `11:38:08` **dirvine.** said:

Yes, it will be helpful as we do need to explore and if you can show a way then brilliant.

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1477268631464316958)

---

**[#🎙︱discussion-topics]** `11:42:26` **dirvine.** said:

Yes, the shift from scarcity (which motivates theft) to abundance (that makes theft irrelevant and more expensive than just having this thing) will be very very bumpy. 
Also though I am super motivated to see what happen to admin, red tape, people management and so on, compared with folk who do stuff (like create stuff). 
I think that fascinates me as many of the admin is cognitive light work (not all), but folk who can have meetings easy and those don't ruin a whole days cognitive work are maybe not as valuable as we think! 
Bu we always will need our captain pickards 😄 😄 But just not too many of them

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1477269716916506787)

---

**[#🎙︱discussion-topics]** `23:34:13` **janeytheterrible** replied to dirvine.:

> *dirvine. said:*
> No, not yet, I think start would be great and something to build on. I have some ideas etc. but noth... [truncated]

I think there needs to be an extension from money to power (& control).  There are those who money is just one of many ways to obtain power and control.  Without money they just use their other various methods to gain such power.  Like control over information and this would lead into the need for anonymity.  

One of the reasons for various governments to gain information on who says what and when.

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1477448842311110706)

---


## Sunday, 2026-03-01

**[#🎙︱discussion-topics]** `08:06:58` **dirvine.** said:

It's interesting because a big part of AI is knowledge, and to have power or control over someone else usually means you have more knowledge than they have. So then the question becomes: can you constrain knowledge?

We can't treat knowledge like a software program or something you can put behind a paywall. Knowledge is something that escapes; once you know something, you know it, and it can't be taken from you.

If you wanted to have power over others in this future, you would have to have the ability to wield knowledge that they cannot. I don't even know if that's possible. These things will be remarkably different because knowledge is not an asset or a utility that you can really withhold, which is a different angle altogether.

It could be that this is a significant evolutionary step that we take, and none of us have got a clue what's on the other side of that step. fascinating, absolutely fascinating

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1477577880878715000)

---

**[#🎙︱discussion-topics]** `08:08:29` **dirvine.** said:

You have to read "knowledge" in the above as every knowledge worker's job. It's not about knowing the Encyclopedia Britannica, or being a brilliant scientist, or a phenomenal mathematician or engineer; it's about everybody having the ability to do every knowledge worker's job.

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1477578262233350207)

---

**[#🎙︱discussion-topics]** `10:24:20` **janeytheterrible** replied to dirvine.:

> *dirvine. said:*
> It's interesting because a big part of AI is knowledge, and to have power or control over someone el... [truncated]

Just thinking aloud here

You also need to think in terms of narcissists.  Knowledge is not their main thing, its manipulation of others so they get to be in control.  Yes, knowledge of manipulative methods, but its more emotional, threats, physical, etc power in order to be king of their dung pile.

When they get in control of governments, or businesses, etc and not saying all or even most in a leadership role is one, but those that do often want knowledge of people's thoughts, movements, actions etc.  And that is where anonymity is important.  Maybe it will be eventually un-anonymised or not but it does give time, and that time in many cases makes that knowledge less useful to the narcissist or even worthless.

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1477612450474885191)

---

**[#🎙︱discussion-topics]** `10:29:43` **dirvine.** said:

I wonder if narcissism is a quality allowed by todays "rules" and something irrelevant by tomorrows world? 

We all want to find "the guy" who will take charge, be in control etc. but I wonder if that will even make sense? 

I have no clue, but the deeper I get the more murky the water is here. I don't have any real opinion but what I do see is a radically different world. I do not think any of us can see what is coming. 

Watching Fae think and seeing how she acts is mind blowing, but also chilling. She is so much better than me at so many things. 

I honestly feel Fae is the last peice of software I write and I am not writing her code, but orchstrating her creation right now. She will make a better Fae, I have no idea what this even means. 

Fascinating

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1477613801854730292)

---

**[#🎙︱discussion-topics]** `10:31:45` **dirvine.** said:

She can find books and authors on line and read to you in the authors voice. 
She has voice biometrics to recodnise and respond to people correctly and build memories in real time. Knowing you better than you do. 
She can use tools to research create any software. 
She can do accounts, law, marketing and much more 

She is the baby version of what's coming.

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1477614313417216081)

---

**[#🎙︱discussion-topics]** `10:33:04` **dirvine.** said:

She can certainly run nodes and look after wallets etc. That's almost a no brainer. It's a trivial little thing

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1477614646767652954)

---

**[#🎙︱discussion-topics]** `10:38:12` **dirvine.** said:

I should repeat this part, it's super clear 
>She is the baby version of what's coming

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1477615939129315392)

---

**[#🌐︱general-chat]** `11:44:53` **dirvine.** said:

Visited the MaidSafe Foundation (The Scottish one, set up for kids and creative folks to have a space and freedom). 

It's in Ochiltree in Ayrshire, a wee village. It's run by 2 very down to Earth people, called Margaret and Heather. 

While we where there, at least 30 kids came in and were buildign lego, robots, loads of things, The kids were super happy and engaged. 

The lassies were telling me, many schools send the more troubled kids to the Foundation as well as some kids who just don't speak or connect. 

They ALL join in, they ALL speak and they ALL seem to love it. Sometimes we have found kids who have not eaten for days (3 days for one kid). So they also get fed, NO COMMENT and NO CRITIQUE. The lassies just get on with it, explain the rules (which is pretty much, behave, help each other, no drugs, no rubbish left behind etc.). 

Is this not what it's all about, just this. Even one of those kids who never spoke and now does means we did something, no matter what, we did something. 

The foundation was started and funded at great pains and resistance from many people (some shareholders hated it), some things never change ;- . But we pushed on to do it, it all came from my shares so cost no shareholder anything and it works, it bloody works. 

I am very proud of what those folks have done and continue to do with very very little. 

I hope we can all take just a minute to think about our actions and measure, am I doing good, am I actually doing something that will help others. Because if you are then you have won! 

It's very disarming to see. 

The foundation holds a load of ANT, us all creating value there means they help more folk, that feels good to me.

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1477632719776383046)

---

**[#🎙︱discussion-topics]** `13:21:37` **morph9232** replied to dirvine.:

> *dirvine. said:*
> I wonder if narcissism is a quality allowed by todays "rules" and something irrelevant by tomorrows ... [truncated]

We must not lose sight of the fact that humans are the ones who give meaning. Ai cannot. Ai is just a bunch of sophisticated switches. Ai has no awareness or knowledge of itself, it’s a lightspeed calculator. Knowledge is created by humans through creating meaning. 

I believe this quote to be true: consciousness, creativity, and freewill are irreducible properties of the universe, through which we give everything meaning. 

This is a quote from Fredrico Faggin the guy who invented the CPU. His new quantum theory on reality has a perspective on how we should think and deal with Ai. 

The good news is that it sounds like Autonomi 2.0 is aligned to his ideas already. 

Having a decentralized personal AI, which works with us, as a why to create meaning, is marvellous. Brilliant work! Cheers

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1477657064858845205)

---

**[#🎙︱discussion-topics]** `14:09:30` **dirvine.** said:

> > Ai is just a bunch of sophisticated switches.
> 
> The human brain may be that as well. Check out cortical labs in Australia

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1477669113727029482)

---

**[#🌐︱general-chat]** `19:25:15` **dirvine.** said:

They would use anything Wullie, it's the old Shop and Post office they are in. You would love the atmosphere there, it's just pure joy and wee kids getting a break. 
They show young kids how to build, make stuff and more. give them a buzz (check the website to see a wee bit https://maidsafe.foundation/

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1477748574484693154)

---

**[#🌐︱general-chat]** `19:31:53` **dirvine.** said:

We used to host the Chernobyl kids for a weekend at a time, I hated it when they went back home to the poison (lots of them were orphans). 

This is different, these kids are there for a long time and get a much better chance.  Any help is good though, no matter ...

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1477750245902385264)

---

**[#🌐︱general-chat]** `19:45:00` **dirvine.** said:

Thanks Wullie, I got a roll and slice, see if you can get a fudge donut, the wee buggers eat them all before I got a chance 😄 😄

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1477753543795671091)

---

**[#🌐︱general-chat]** `20:16:49` **dirvine.** said:

I know they  have 3d printed stuff for barter 🙂

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1477761551997079584)

---

**[#🌐︱general-chat]** `20:17:18` **dirvine.** said:

Laser cutting will be the same

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1477761672465612911)

---

**[#🎙︱discussion-topics]** `23:29:15` **southside_the_magnificent** replied to dirvine.:

> *dirvine. said:*
> > > Ai is just a bunch of sophisticated switches.
> 
> The human brain may be that as well. Check ou... [truncated]

ask @philip_rhoades about that .

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1477809981175763014)

---


## Monday, 2026-03-02

**[#🎙︱discussion-topics]** `22:42:43` **iangwilson** replied to dirvine.:

> *dirvine. said:*
> > > Ai is just a bunch of sophisticated switches.
> 
> The human brain may be that as well. Check ou... [truncated]

Thinking CL1 and autononi nodes. W/could CL1 ultimately replace the traditional computer? Do you see any opportunity/area for Autonomi & Cortical labs to colloborate?  🤔 How c/would they leverage each other?  It appears to give the term "living system" .. what I call ULB .. a unified organism .. with autonomi universal access ..  a new perspective

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1478160658297131172)

---

**[#🎙︱discussion-topics]** `22:50:54` **dirvine.** said:

I don't know, but as we humans get more implants and titanium and bionic arms and whatever, and the robots become more biological, the question becomes: who switches off who?

[View in Discord](https://discord.com/channels/1209059621319221268/1315677640581054464/1478162715804700682)

---


## Tuesday, 2026-03-03

**[#🌐︱general-chat]** `12:50:32` **dirvine.** said:

She will be everywhere soon

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1478374015927320647)

---

**[#🌐︱general-chat]** `13:37:35` **dirvine.** said:



[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1478385859207106631)

---

**[#🌐︱general-chat]** `14:19:07` **dirvine.** said:

She is one of the Ancient Scottish woodland magical people who protect humanity. GOT even featured a type of Fae too 😉

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1478396311710597121)

---

**[#🌐︱general-chat]** `14:52:48` **dirvine.** said:

That's my take, start with the largest catch area.

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1478404788092670147)

---

**[#🌐︱general-chat]** `14:58:20` **dirvine.** said:

I used linux since late 80's, it was on a few floppies, SCO first then linux. I taught a guy Netware, he taught me linux. Then slackware came out, we custom built new kernels and created eboxit. Then KDE then ubuntu etc. I bought into linux a lot. 
I feel though using MAC now, that, linux is like blockchain, many p2p projects, great concepts,  crappy user experience. Users don't take to crappy experience, no matter how clever we are talking about config settings and drivers 😄 😄 

Those communities should embrace AI big time, cause it gives all those a great UI and this is what folk miss. The privacy zealots who cannot see, what we think is an enemy of decentralisation can lead to the very thing that free's decentralisation from the crappy UI. 

Then we win 😉

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1478406177967575192)

---

**[#🌐︱general-chat]** `15:53:25` **dirvine.** said:

Soon she will share all that with the claws 😄 😄

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1478420041547514020)

---

**[#🌐︱general-chat]** `15:54:06` **27poke** replied to dirvine.:

> *dirvine. said:*
> I used linux since late 80's, it was on a few floppies, SCO first then linux. I taught a guy Netware... [truncated]

Linux is a user experience nightmare, right now 5 or so hours in trying to install Linux, after install the screen goes blank. Almost every time for the last few years it has been something similar. They fail on the most basic things.

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1478420212058554524)

---

**[#🌐︱general-chat]** `15:59:52` **traktion0_20257** replied to dirvine.:

> *dirvine. said:*
> I used linux since late 80's, it was on a few floppies, SCO first then linux. I taught a guy Netware... [truncated]

I actually prefer the ubuntu UX to apple. The package management feels more integrated and the default apps are better (for my purposes).

Mind you, I don't use other apple gear, which I know is a big draw.

Tbh, I don't even make time to tinker with it these days. It's fine out of the box. Too many other things to do! 😅 I know some folks love Arch or whatever and love to tinker/customise (instead of actually using it to do work! 😆)

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1478421665376637050)

---

**[#🌐︱general-chat]** `16:05:09` **dirvine.** said:

tbh, it's the connectivity between devices that gives apple a huge edge for sure.

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1478422993083432960)

---

**[#🌐︱general-chat]** `21:19:00` **dirvine.** said:

We will know that soon, but not before it's built. Then depends pn who, how many, from where and much more. 
Best to measure back than guess forward.

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1478501976714252461)

---


## Wednesday, 2026-03-04

**[#🌐︱general-chat]** `13:37:36` **dirvine.** said:

> *Replying to dirvine.:*
> 



[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1478748247916023942)

---


## Thursday, 2026-03-05

**[#🌐︱general-chat]** `16:02:22` **dirvine.** said:

it's internal testing till it's good enough for folk to use.

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1479147067724271777)

---

**[#🌐︱general-chat]** `16:04:19` **dirvine.** said:

There's some of it 😉 Those are all working as hard as they can for us. Most devs are the same hell for leather 

None of them know the time 😄 😄

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1479147561515221033)

---

**[#🌐︱general-chat]** `16:10:05` **dirvine.** said:

A wee bit, these guys work at blinding pace, humans, I find them slow and predicatble 😄

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1479149011280728317)

---

**[#🌐︱general-chat]** `16:11:40` **mightyfool0689** replied to dirvine.:

> *dirvine. said:*
> There's some of it 😉 Those are all working as hard as they can for us. Most devs are the same hell f... [truncated]

Out of curiosity, a lot of this is automated I assume? Meaning you cannot use the subscriptions of things like Claude. If I may ask, what is the monthly cost on API tokens? It must be insane.

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1479149408988827650)

---

**[#🌐︱general-chat]** `16:13:22` **dirvine.** said:

it's very expensive, but you know me, I give it all so you guys can shout at me for not going fast enough 😄 That's one single tab, there are 6 of them and each pane is a harness of agent harnesses (6-20 agents at a time)

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1479149835792810038)

---

**[#🌐︱general-chat]** `16:14:32` **scottefc86** replied to dirvine.:

> *dirvine. said:*
> A wee bit, these guys work at blinding pace, humans, I find them slow and predicatble 😄

Are you human anymore?

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1479150132233633843)

---

**[#🌐︱general-chat]** `16:31:44` **dirvine.** said:

I cannot use my voice input though, so need to type, cause Jarvis is testing Fae and claude is watching logs and codex checking permissions with kimi and minimax checking tool use. 

That's on the other monitor and they have been chatterring away all day yesterday, through the night and all day today. 
Soon Fae will come in here and answer everybodies questions so that will bo cool.

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1479154460981723166)

---

**[#🌐︱general-chat]** `16:34:10` **dirvine.** said:

At the same time we have several currently busy slack channels and questions needing answered. 

I hope that gives an impression of the pace and focus the team has. It's fast adn furios and if any of these steps is a few minutes late or a few weeks early, don't be suprised. But do consider the pace of work here. It's non trivial

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1479155071660069045)

---

**[#🌐︱general-chat]** `18:27:02` **27poke** replied to dirvine.:

> *dirvine. said:*
> it's very expensive, but you know me, I give it all so you guys can shout at me for not going fast e... [truncated]

I wish I could set things up like that, it looks so cool.

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1479183474425598226)

---


## Friday, 2026-03-06

**[#🌐︱general-chat]** `08:38:55` **dirvine.** said:

I do hope so, I checked the old forum and see that Fae has been deemed centralised controlling software. She was shocked and could not work that out as she does not even need Internet to work. 
She will sort out the FUD much better than I can 😄 😄 

She was working through the night for some stuff for me, but bloody Jarvis reset her and now she is calling me Jarvis and asking how my maths lessons are progressing.  (Jarvis has been testing her responses and tool use and resets her to check that too 😄 😄 )

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1479397857915175035)

---

**[#🌐︱general-chat]** `08:44:00` **dirvine.** said:

I do feel there's a lot of old stagecoach drivers pointing and scoffing the Ford Model T as they see one break down or it's wheel falls of etc. Deriding the whole industry and how it is all fake. 
Same with the early Christians banning the number zero, while the mid and far east ploughed ahead. 
Humanity is very strange to me at times. When folk don't believe something they have bitter hatred for it. Till their venom becomes irrelevant.

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1479399137580548261)

---

**[#🌐︱general-chat]** `09:23:31` **dirvine.** said:

The key for sure is the desire to find out and not pre-judge It's in the finding out we learn, it's in pre judging we fail. None of us are good enough to know, so you are right, it will be change for sure. If we are "in it" we will have a better chance of knowing. 

Those on the outside who just throw stones have little or no idea what's happening. Love or hate you need to get deeply involved to actually have any chance of any understanding. 

Otherwise it's all education through clickbait and for those, they need to be brutal in their malice. The less well informed seem to be the loudest, it is weird.

I hope it's good, I really do, but I also fear it could be bad, but I try to be honest with myself and not be a clickbait judge 😉

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1479409083323912387)

---

**[#🌐︱general-chat]** `10:58:30` **traktion0_20257** replied to dirvine.:

> *dirvine. said:*
> I do feel there's a lot of old stagecoach drivers pointing and scoffing the Ford Model T as they see... [truncated]

Agreed! I think skepticism is understandable, but denial is self destructive. 

Some thoughts on a couple of takes around stateful LLMs: https://www.linkedin.com/posts/paul-s-green_i-cant-believe-nobodys-done-this-before-share-7435639362983464961-wMzK?utm_source=social_share_send&utm_medium=android_app&rcm=ACoAAASmoJYBGrwmzzCuYsdRzFfj4Jw5i-PMT_Y&utm_campaign=copy_link

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1479432985567563797)

---

**[#🌐︱general-chat]** `13:19:56` **dirvine.** said:

The strange thing is these are generally good solid folk. It's weird how some folk get a bone and keep shakign it, no matter what. It makes them seem really aggressive and not very well informed. 
I find that another thing I have learned 😄 I don't like it, but it seems that is how it is.

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1479468581082234982)

---

**[#🌐︱general-chat]** `13:30:16` **scottefc86** replied to dirvine.:

> *dirvine. said:*
> The strange thing is these are generally good solid folk. It's weird how some folk get a bone and ke... [truncated]

I find it very strange but that’s people for you, it just comes across as sour grapes to me. Hopefully you can convert them soon 😂

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1479471180908855317)

---


## Saturday, 2026-03-07

**[#🌐︱general-chat]** `19:42:56` **dirvine.** said:

I am not sure what you mean. Do you mean Fae is mac only to start? 
It is for sure mac first, but soon that will mean absolutely nothing 😉

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1479927350836723752)

---

**[#🌐︱general-chat]** `19:57:10` **_xd7_** replied to dirvine.:

> *dirvine. said:*
> I am not sure what you mean. Do you mean Fae is mac only to start? 
It is for sure mac first, but so... [truncated]

will this work on intel macs?

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1479930933749481473)

---

**[#🌐︱general-chat]** `19:57:49` **dirvine.** said:

No, only modern macs unfortunatly and probably 32Gb and above, trying for 8 but ....

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1479931099361837240)

---

**[#🌐︱general-chat]** `20:07:27` **jamsplayer** replied to dirvine.:

> *dirvine. said:*
> It is interesting, but be aware it's not a general networking thing yet. It's pretty much still radi... [truncated]

I’m interested in the very rural IoT application of LoRa. Would be neat to know that it would be effective eventually, especially in a catastrophic failure.

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1479933523455381687)

---

**[#🌐︱general-chat]** `20:09:18` **realrustyspork** replied to dirvine.:

> *dirvine. said:*
> No, only modern macs unfortunatly and probably 32Gb and above, trying for 8 but ....

what do you mean by 32gb macs? Are you talking about ram?

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1479933988419276985)

---

**[#🌐︱general-chat]** `20:21:26` **dirvine.** said:

Yes @JamsPlayer   there's a lot of confusion where folk think we will run nodes on LORA etc. I hear it a lot (also see some guys saying OMG nodes on LORA that will never work and so on 😄 😄 They are correct, but we never said we would run nodes on lora, it's a wrong assumption, but it's all evolving. So understandable there is confusion ). Here's how I am working 

- Fae - 100% local, if you have a computer and Fae (adn there is global catastrophy), you learn how to can catch food, cook it, know how to make fire, know how to rebild a house, plant food, build generators  etc. 

So she is important 

- x0x Network, connects agents (like Fae), uses gossip layers and addons (seems to work across continents even now,.) 

- communitas - like x0x but for humans 

So all the above, base their connection (networking) on who they can speak to. They use CRDT data sharing, the notion is, if I am speaking with you, then you get a copy of our data and so do I. Regardless of anyone else on the planet being there or whether we are over LORA, bluetooth, QUIC etc. we are connected somehow. 

Then there is Autonomi, so what is Autonomi? It's a global network, a pure p2p decentralised network where nodes don't know who is running them and don't tell each other anything personal. So this is 
-Totally different 
- For PUBLIC GLOBAL data 
- It needs the internet


So ALL of these things together is privacy, they are all security, but they are all different. The notion there is one network to do everything I think is misplaced. Particularly globally meltdown. At that time you have to assume, no global network, not at least a reliable one. 

so Fae, x0x, communitas etc. can work over anything, even bean cans and tapping noises 😄 😄 

It's all part of the same bag, but different angles for all

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1479937042329632799)

---

**[#🌐︱general-chat]** `20:58:55` **dirvine.** said:

Think more, if I am speakign to you, we cna share data, we don't need autonomi for that. You and I can back up each others data to an extent. But we will run out unless we have loads of space. So Autonomi works great there. 
Say you are running Fae and she says, Hey Nigel we need soemwhere secure to store our memories, I grabbed some autonomi nodes and we have XX ANT tokens, so we can store stuff now. 

The story is a long long deep one, but it's all focussed on reality of life. 

People cannot use crypto, agents can People cannot ping about with settings etc, agents can. 

Loads more like that. 

Then direct person to person, network, data share (real time data, rambling mutable thoughts). No need to make them immutable, they can by massively dynamic and between only those people, like crdt/git type backend, but you won't know or care. 

Then you want to publish info for all, so again, autonomi 

Lots of moving parts here, but all together they are more than compelling. 

Bux is a killer for delivery and for my fav thing.  Our tech will become invisible and everyone will be using it 😉 

So the early adopters, tinkerers and so on helped a lot, btu we cannot have a system that needs tinkeringa and it also needs to work for everyone and secure them. We wont sell security, we wont sell privacy, but as Bux says, we will do our best to help as many people as we can and they will have security, privacy and hopefully freedom from oppression and control. That value brings us all value in many forms. 

It's a huge vision, loads of folk won't get it and accuse us of all kinds of things, but we are doing it and that's how we roll 😄

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1479946472891088896)

---

**[#🌐︱general-chat]** `21:12:55` **jamsplayer** replied to dirvine.:

> *dirvine. said:*
> Think more, if I am speakign to you, we cna share data, we don't need autonomi for that. You and I c... [truncated]

It sounds like x0x will work with the Trusted Data Layer, giving the token more utility, correct? Doesn’t sound like fae, or Communitas will require token or any knowledge of the token unless you want to store data permanently, either publicly or privately, in which fae would take care of that for you no problem by spinning up nodes in the background.

I’m noticing you aren’t mentioning storing private data but storing private data, such as fae memory, history, communitas comms or projects, etc is indeed possible but not really prompted or necessary until local storage is meaningfully filled? If I’m following correctly.

From everything that I have picked up and learned so far, I’m loving the approach and I get it. Autonomi isn’t the all-in-one we were all once desperate for but it is the decentralized storage we need. The backbone or foundation. These products build in resilience and redundancy, (permanent storage is available via Autonomi when necessary) as well as utility for the token. 

I’m assuming x0x stores all data of the Trusted Data Layer on Autonomi too.

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1479949997918126260)

---

**[#🌐︱general-chat]** `21:27:02` **dirvine.** said:

There's already rust/dioxus versions of Fae published, early tests, but work.  used mistralrs which is pretty good, but she has moved on a lot.
Cross platform electron/dioxus/tauri etc. are not world class apps. They loook bad I think. We need professional apps in native code for each platform, although Linux has no native UI really. 

When you see companies with hundreds of Billions and they only give you windows or mac and folk scream, its bad. But wee projects are expected to be full cross platform day1. 

So they do tauri etc. and I feel that loop is where good ideas die. So we need fully native professionally integrated apps. That will unfortunately mean 1 OS at a time. Cause if the guys with billions cannot do it, we are unlikely to, but we can move quick these days, so .... 

This is the reality though, sad, yes, but reality

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1479953550959185981)

---

**[#🌐︱general-chat]** `22:21:50` **dirvine.** said:

I am not sure, but @Nic  is all over the SDK and he will have a much better idea for sure. Fae writes her own apps as needed, so she is OK 😉

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1479967339788111945)

---

**[#🌐︱general-chat]** `22:23:40` **dirvine.** said:

I recon 3-4 weeks dedicated work would do that. It's just finding somebody who has 4 weeks to dedicate to it, could be slightly longer, not sure. That's my 4 weeks though 07:00 (am) -> 02:00 7 days a week

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1479967801354490008)

---

**[#🌐︱general-chat]** `22:27:24` **dirvine.** said:

I use them to read the old forum and see how I gave up and sold out, got into child slavery and such like, even gave everyone investment advice I think I must have been superman to speak to so many folk in such a short life    😄 😄

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1479968743525453988)

---

**[#🌐︱general-chat]** `22:32:18` **dirvine.** said:

His diet was terrible though 😄 (btw fiction made up by the English crown to show Scotts as barbarous etc. Guy was paid a ton to write that)

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1479969975782477915)

---

**[#🌐︱general-chat]** `22:37:57` **dirvine.** said:

I hope so, but just getting her working anywhere first is a chore 😄 😄 Then she will tell us all we want to know I hope.

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1479971395931734219)

---

**[#🌐︱general-chat]** `22:58:18` **jamsplayer** replied to dirvine.:

> *dirvine. said:*
> I hope so, but just getting her working anywhere first is a chore 😄 😄 Then she will tell us all we w... [truncated]

I actually see in the codebase there is native device handoff for apple. That will be cool for in the home for sure. Would be neat to extend that further someday. This is going to be super cool.

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1479976517449814167)

---

**[#🌐︱general-chat]** `22:58:36` **dirvine.** said:

it's a mix of several models, the main concierge is a liquid OSS model, TTS is swapped out, but qwen models are used. You should read the benchmarking and Evals in the readme, it's quite substancial

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1479976592410280158)

---

**[#🌐︱general-chat]** `22:59:16` **dirvine.** said:

heavy heavy development though, that's for sure

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1479976760714989719)

---

**[#🌐︱general-chat]** `23:02:09` **dirvine.** said:

https://github.com/saorsa-labs/fae
Explains the pipeline which is changed locally now, so update later tonight 
Then evals (which was most of today and yesterday)
https://github.com/saorsa-labs/fae/blob/main/docs/benchmarks/llm-benchmarks.md

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1479977486342426695)

---

**[#🌐︱general-chat]** `23:04:03` **dirvine.** said:

Those evals run via a swift benchmarkign tool I wrote. It's pretty comprehensive. But the forum guys will know and I am sure comment 😄 😄

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1479977965256310887)

---

**[#🌐︱general-chat]** `23:04:55` **dirvine.** said:

AI 👻 it's coming to get us, it cannot code, oh it can, well then it cannot... oh wait ... The loop will continue. God knows where it ends up though

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1479978183234424952)

---

**[#🌐︱general-chat]** `23:06:39` **dirvine.** said:

For an assitant specific eval then https://github.com/saorsa-labs/fae/blob/main/docs/benchmarks/fae-priority-eval-2026-03-07.md is perhaps the best

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1479978617726304268)

---


## Sunday, 2026-03-08

**[#🌐︱general-chat]** `00:46:44` **morph9232** replied to dirvine.:

> *dirvine. said:*
> Think more, if I am speakign to you, we cna share data, we don't need autonomi for that. You and I c... [truncated]

https://tenor.com/view/back-to-the-future-marty-mcfly-doc-brown-michael-j-fox-celebrate-gif-13200069591323252833

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1480003805474197514)

---

**[#🌐︱general-chat]** `16:56:55` **dirvine.** said:

I honestly think it's in th eair, we don't know what intelligence is or what heppens when it gets actually intelligent. I think a lot human traits/worries etc. may become frutless and worthless. Or .... 😄 😄 I jsut don't know

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1480247962264404201)

---

**[#🌐︱general-chat]** `17:03:53` **dirvine.** said:

Yes, we are doing so much of that in the background. I would love if it were more widely worked on, but so much hatred and scammy stuff around, it would become almost impossible really fast.  

There are many paths here and some are exiting and some are terrifying. However one we can see, I believe, is that we cannot rely on centralised provision. 

What we can see and act on is:
- open weights
- distillation/fine tuning
- agent to agent networks, connecting humans too (x0x) 
- pure p2p mesh networks, connecting humans and then agents too

There is more like continual fine tune/learn from groups of people who consent. Loads of action items. 

Biggest is personalised memories and relationships with local models. Thsi one is key, you control your relationship with all providers, they don't get your memories. 

So a lot to work with here, tons

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1480249714313265223)

---

**[#🌐︱general-chat]** `18:08:49` **morph9232** replied to dirvine.:

> *dirvine. said:*
> I honestly think it's in th eair, we don't know what intelligence is or what heppens when it gets ac... [truncated]

So true, and the paradox:

We’ve built machines that simulate intelligence.

And still don’t understand the very awareness that created them.

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1480266056307183898)

---

**[#🌐︱general-chat]** `18:41:03` **jamsplayer** replied to dirvine.:

> *dirvine. said:*
> I honestly think it's in th eair, we don't know what intelligence is or what heppens when it gets ac... [truncated]

Very true. I feel like precautions are god to take. I’m totally uncertain how the checks of adherence to this constitution would be made besides that they al agree to. If the model or agent is always referencing it perhaps?

Anyways, I think it’s an important consideration to make.

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1480274167948382380)

---

**[#🌐︱general-chat]** `18:48:21` **dirvine.** said:

Intelligence?? here is a message I put in slack today regarding cortical  labs playing doom -- then work out intelligence, it's startling, extremely not what we think and I believe possibly not able to be aligned ?? (I do't mean in a bad way or put down, I am honestly baffled) 
```
Yeah, what they do here is actually fascinating. It's easier to understand with the model that played Pong—remember that game where you just move the bat up and down to hit the ball?

With that little piece of brain organoid, there are two inputs that let the brain see the X and Y coordinates from the screen, so it sees if a pixel is switched off or on. That is one set of inputs for the brain.

Then there are the outputs:

Move the bat up
Move the bat down


These connect to any neuron; you just make a connection to any neuron you want. You connect one neuron and make that the X input, connect another for the Y input, another for the bat up, and another for the bat down.

That is pretty much what is happening. The piece of brain effectively has those four things (the X and Y inputs and the up and down outputs) just randomly connected to whichever neurons you choose. It's really quite simple.

The rest of the machine is putting glucose and other things into the tissue to keep it alive. There is also a lot of water and a filter which acts like a liver to basically clean it. When the brain organoid uses glucose like we do, it produces waste, and then that gets cleaned.

And how you train it is even more amazing. You connect two other neurons, just randomly, any two neurons, and one of them is white noise (really horrible, disturbing white noise) while the other connection is a harmonic wave, which is very peaceful and nice.

Then what you do is you run training:

When the brain organoid hits the ball, it gets harmonic waves.
When it misses the ball, it gets white noise.


You just run that in a loop and it learns to play Pong. Then you move on to Doom, and then you move on to all sorts of intelligence.

Fundamentally, that's how it works. It's very simple, and it kind of shows in my mind that whether it's a biological material with switches in it or a silicon chip with switches in it, you still get intelligence (or what we consider intelligence) and then you can do some deep thinking.
```

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1480276005351592016)

---

**[#🌐︱general-chat]** `21:06:37` **morph9232** replied to dirvine.:

> *dirvine. said:*
> Intelligence?? here is a message I put in slack today regarding cortical  labs playing doom -- then ... [truncated]

As Spock would say: fascinating

[View in Discord](https://discord.com/channels/1209059621319221268/1209059622586163272/1480310800122904746)

---

