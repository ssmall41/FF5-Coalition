# Coalition

## Introduction 
Coalition is a project for generating multiple parties for challenge runs of FF5. All parties are intended to be Four Job Fiesta type of runs. 

[Four Job Fiesta](https://www.rpgsite.net/feature/11964-final-fantasy-v-four-job-fiesta-guide-how-to-tackle-this-unique-challenge) is a “challenge mode” for FF5. 
Instead of playing the game as normal, participants are assigned 4 jobs randomly (with some rules) that their characters 1) are allowed to use, and 2) must use. 
Completing a run is as simple as defeating ExDeath while only using assigned jobs.

This play style is popularized by the yearly [FF5 Four Job Fiesta charity event](https://www.fourjobfiesta.com/). Participants in the 
charity event are not restricted to a single run. In fact, many participants make several runs. Although some settings can be tweaked, 
jobs are always assigned randomly, meaning each run is extremely likely to offer a unique combination of jobs.

However, not all combinations of jobs are completely unique in terms of play style. For example, Knight / Berserker / Ranger / Dragoon will have a 
similar play style to Knight / Mystic Knight / Ninja / Samurai; both parties are oriented towards physical attacks. Some jobs are known to be “broken”, 
which means any party that includes them will be played similarly. For example, a winnable strategy for a party with a Summoner is for each character to 
learn the !Summon ability and rely on that for almost every situation, with the other three jobs having much less importance. Not much skill is required of 
the player to implement this strategy. The same can be said for the Chemist job and its !Mix ability. 

The goal of Coalition is to produce a set of parties that are “different” from each other so that players can complete multiple Four Job 
Fiesta runs while experiencing different challenges from each. 

## How to Use Coalition
A proof of concept is [available online](https://sites.google.com/view/ff5-fjf-selector/home), and feedback is appreciated. The Coalition website will allow 
players to select a play style (for now, Regular, Meteor, or Meteor with Duplicates) and receive a collection of five unique parties. 
There’s no unlocking jobs like in the Four Job Fiesta event. 

My goal here is to collect feedback on the quality of parties produced and understand whether others think they are really “different” 
from each other. To be clear: I have no intention of making the website nicer by unlocking jobs or storing assignment histories. 
That would be reproducing the Four Job Fiesta site, and I have no interest in doing so. 

To provide feedback: if you've got a GitHub account, you can leave your feedback in an [issue](https://github.com/ssmall41/FF5FJF-Selector/issues) on the project. 

## How Does It Work?
Once a play style is selected, the first party is decided completely randomly. Note that there is no special weighting to the jobs in the 
party; they’re all equally likely to be chosen, but in line with the rules of the play style. (I mention this because I believe the official event 
has, in the past, not used completely equal weighting for Meteor runs). 

For the second party, Coalition first looks at all possible parties (in line with the play style) and determines which ones are “close” to 
the first party. Those “close” parties are removed from consideration. Then the second party is chosen from the remaining parties. 

The selection process continues in a similar way for further parties. Coalition looks at already chosen parties, removes all “close” 
parties from consideration, and then selects a new party randomly. 

It’s totally possible that after a few parties are chosen, all remaining parties are too “close”. When this happens, Coalition relaxes its 
idea of “closeness” a bit to allow for new parties to be chosen. Theoretically, all possible parties can eventually be chosen using this approach, 
but I doubt anyone has the patience for playing all of them. The website has a built-in limitation of five parties. In the code, this limit can be changed to anything.

## What does “close” mean?
Yeah, that’s pretty much the heart and soul of all this. There isn’t a 100% perfect way to define closeness between two parties, and any 
measure used is up for debate. I’ll give the high-level idea here, but if you’re a fiend for details, check <here in the code> to see the exact definitions.

Every party is represented in the code by a collection of numbers called an embedding. (If you want to get into it, mathematically, an 
embedding is a vector in R^d with d in the current website being x.) The code here generates every possible party and calculates an appropriate 
embedding. With the embeddings in place, it’s possible to compare two parties and say how far apart they are.

So how does the code calculate the embeddings? That takes into consideration the jobs in the party, and the order in which they are assigned. 
Right now, the code takes into account the following: 

* jobs in the party and how many (important for runs allowing Duplicates),
* the number of each style of job available in the party after each crystal (style means Heavy, Clothes, Mage, or Misc, with Misc being Mime and Freelancer), and 
* the weapon types that the party can use after each crystal whether an available job can use a shield at each crystal.

* For Meteor runs, it’s possible that no jobs are available after a crystal and the party must consist of only Freelancers. Coalition takes this into account. 

## FAQs

### Are you affiliated with the official Four Job Fiesta?
Nope. I’ve participated the last several years, but I have nothing to do with administration of the event at all. I’m just playing Final Fantasy. 

### Why did you make this?
I saw in the official FJF Discord channel several discussions about “gauntlet runs”, where participants would try to play every job at least 
once. I also noticed participants making multiple (in some cases, more than 10) runs per event. When multiple runs happen, it becomes likely 
that some will be very similar in style, and that’s not interesting. Personally when I play, I’m always praying to the RNG gods to get something 
different so that I’m not just playing the same game over and over. It keeps things interesting. 

### Why don’t you include job skills when defining “closeness”?
The challenge with including skills is that they are almost entirely determined by the job that provides them, so just checking which 
jobs are in the party covers this. For example, TwoHanded comes from the Knight job; no other job teaches it. If a party has a Knight, 
TwoHanded is on the table.  There are a few small exceptions, like !Flee and !Smoke are functionally the same, and !Red overlaps a bit 
with !White and !Black. But really, I don’t expect to get much value by including skills. 

### Are there other things that could be considered in the “closeness” definition?
Yep. This topic is a bit open-ended. Some stuff I can think of off the top of my head:
Inflicting statuses: what statuses can a party inflict on enemies? For example, the Atmos battle is made simple when the party can put 
it to sleep. This is limited to parties with access to Swords and !Black.
Broken jobs: 

### The third party I generated has the same job from the second party. What gives?
Coalition is not the same as gauntlet runs, where every party has a unique set of jobs. The same job could be selected for 
multiple parties, but the parties themselves will play differently. That said, one way to make parties play differently is to use different jobs, 
so 5 parties will see most of the jobs appearing. 






