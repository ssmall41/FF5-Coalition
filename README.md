# Coalition

## Introduction 
Coalition is a project for generating multiple parties for challenge runs of [Final Fantasy 5 (FF5)](https://en.wikipedia.org/wiki/Final_Fantasy_V). All parties 
are intended to be Four Job Fiesta type of runs. Two types of runs are included here: Gauntlet and Coalition.

[Four Job Fiesta](https://www.rpgsite.net/feature/11964-final-fantasy-v-four-job-fiesta-guide-how-to-tackle-this-unique-challenge) is a “challenge mode” for FF5. 
Instead of playing the game as normal, participants are assigned 4 jobs randomly (with some rules) that their characters 1) are allowed to use, and 2) must use. 
Completing a run is as simple as defeating ExDeath while only using assigned jobs.

This play style is popularized by the yearly [FF5 Four Job Fiesta charity event](https://www.fourjobfiesta.com/). Participants in the 
charity event are not restricted to a single run. In fact, many participants make several runs. Although some settings can be tweaked, 
jobs are always assigned randomly, meaning each run is extremely likely to offer a unique combination of jobs.

However, not all combinations of jobs are completely different in terms of play style. For example, Knight / Berserker / Ranger / Dragoon will have a 
similar play style to Knight / Mystic Knight / Ninja / Samurai; both parties are oriented towards physical attacks. Some jobs are known to be “broken”, 
which means any party that includes them will be played similarly. For example, a winnable strategy for a party with a Summoner is for each character to 
learn the !Summon ability and rely on that for almost every situation, with the other three jobs having much less importance. Not much skill is required of 
the player to implement this strategy. The same can be said for the Chemist job and its !Mix ability. 

The goal of Coalition is to produce a set of parties that are “different” from each other so that players can complete multiple Four Job 
Fiesta runs while experiencing different challenges from each. 

Gauntlet runs are a common way to produce unique parties, and these can also be generated here. Gauntlet runs use each job once in a collection 
of 5 (Meteor) or 6 (Regular) parties. The Mime and Freelancer jobs are excluded. Obviously, if the numbers don't perfectly work, so the 6th party 
will have a few duplicates.

## How to Use Coalition
A proof of concept is [available online](https://sites.google.com/view/ff5-coalition/home), and feedback is appreciated. The Coalition website will allow 
players to select either Gauntlet or Coalition and a play style (Regular, Typhoon, Volcano, and Meteor, and with or without Duplicates), 
and then receive a collection of five unique parties. There’s no unlocking jobs like in the Four Job Fiesta event. 

My goal here is to collect feedback on the quality of parties produced and understand whether others think they are really “different” 
from each other. To be clear: I have no intention of making the website nicer by unlocking jobs or storing assignment histories. 
I have no interest in reproducing the Four Job Fiesta event site.

To provide feedback: you can leave your feedback in a GitHub [issue](https://github.com/ssmall41/FF5FJF-Selector/issues) on the project. I can also be reached on Discord
as yet41.

## How to Use the Code
The codebase for Coalition is written in Python. Clone the Git repository, and then run `pip install -r requirements.txt` in the project folder.
The Jupyter Notebook file `assignment.ipynb` is how I generate parties. Of course, you're welcome to go through the `.py` files to see details.

The Jupyter Notebook file `assignment_gauntlet.ipynb` generates runs following Gauntlet rules.

## How Does It Work?
Once a play style is selected, the first party is decided completely randomly. Note that there is no special weighting to the jobs in the first 
party; they’re all equally likely to be chosen, but in line with the rules of the play style. (I mention this because I believe the official event 
has, in the past, not used completely equal weighting for Meteor runs). 

For the second party, Coalition first looks at all possible parties (in line with the play style) and determines which ones are “close” to 
the first party. Those “close” parties are removed from consideration. Then the second party is chosen from the remaining parties. 

The selection process continues in a similar way for further parties. Coalition looks at already chosen parties, removes all “close” 
parties from consideration, and then selects a new party randomly. 

It’s totally possible that after a few parties are chosen, all remaining parties are too “close” to each other. When this happens, Coalition relaxes its 
idea of closeness a bit to allow for new parties to be chosen. Theoretically, all possible parties can eventually be chosen using this approach, 
but I doubt anyone has the patience for playing all of them. The website has a built-in limitation of five parties. In the code, this limit can be changed to anything.

## What does “close” mean?
Yeah, that’s pretty much the heart and soul of all this. There isn’t a 100% perfect way to define closeness between two parties, and any 
measure used is up for debate. I’ll give the high-level idea here, but if you’re a fiend for details, check <here in the code> to see the exact definitions
in `embeddings.py`.

Every party is represented in the code by a collection of numbers called an embedding. (If you want to get into it, mathematically, an 
embedding is a vector in R^d with d in the current website being x.) The code here generates every possible party and calculates an appropriate 
embedding. With the embeddings in place, it’s possible to compare two parties and say how far apart they are.

So how does the code calculate the embeddings? That takes into consideration the jobs in the party, and the order in which they are assigned. 
Right now, the code takes into account the following: 

* jobs in the party and how many (important for runs allowing Duplicates), with special consideration to "broken" jobs (Black Mage, Summoner, and Chemist),
* the number of each style of job available in the party after each crystal (style means Heavy, Clothes, Mage, or Misc, with Misc being Mime and Freelancer), 
* the weapon types that the party can use after each crystal, and
* whether an available jobs can use a shield at each crystal.

For Volcano and Meteor runs, it’s possible that no jobs are available after a crystal and the party must consist of only Freelancers. Coalition takes this into account. 

## FAQs (or rather, questions I think will be asked)

### Are you affiliated with the official Four Job Fiesta Event?
Nope. I’ve participated the last several years, but I have nothing to do with administration of the event at all. I’m just playing old school Final Fantasy. 

### Why did you make this?
I saw in the FJF Event Discord channel several discussions about “gauntlet runs”, where participants would try to play every job at least 
once. I also noticed participants making multiple (in some cases, more than 10) runs per event. This made me wonder if it would be possible to force party
selection in a way to keep things interesting. Personally when I play multiple runs, I’m praying to 
the RNG gods to get significantly different parties so that I’m not just doing the same thing over and over. It keeps things interesting. 

### Why don’t you include job skills when defining “closeness”?
The challenge with including skills is that they are almost entirely determined by the job that provides them, so just checking which 
jobs are in the party covers this. For example, TwoHanded comes from the Knight job; no other job teaches it. Checking if a party
has a Knight is enough to include TwoHanded in the mix. There are a few small exceptions, like !Flee and !Smoke are functionally the same, and !Red overlaps a bit 
with !White and !Black. But really, I don’t expect to get much value by including skills. 

### Are there other things that could be considered in the “closeness” definition?
Yep. This topic is a bit open-ended. Some stuff I can think of off the top of my head:

* Inflicting statuses: what statuses can a party inflict on enemies? For example, the Atmos battle is simpler when the party can put 
it to sleep. This is limited to parties with access to Swords and !Black, so including which parties have access to sleep could help.
It's similar for other statuses (mute, darkness, instant death, etc.)
* Broken jobs: this is a pretty open topic. For the current version of Coalition, it's less likely (but not impossible) that you'll see 
a Black Mage, Summoner, and Chemist appearing in multiple parties. It's an arbitrary line to draw here: are those really "broken" jobs?
Are there others?

There are probably a million other things to consider. Ideas are always appreciated.

### Can I play with more or less than 5 parties?
Less is easy: just play the parties in the order Coalition website gives them, and stop when you don't want to play anymore.

Coalition is able to generate more than 5 parties, but I limited the website to only 5. You are welcome to use the Python code and
generate a group of 500 parties if you wish.

### I didn't get my favorite job in any of the 5 parties! What gives?
Coalition is not the same as gauntlet runs, where every job shows up at least once. The RNG gods might cause some jobs to not appear in any party, while
the same job could be selected for multiple parties, but the parties themselves will play differently. That said, one way to make parties play differently
is to use different jobs, so 5 parties from Coalition tend to see a variety of jobs. 

## To Do
Some open ideas for the future
* Try neural network based embeddings. An encoder-decoder setup might simplify the embeddings and make comparisons between parties easier. 
However, it's not really clear if this would bring anything useful.
* Do a proper analysis. Show means and stats for different parties compared to random parties. I've done some ad-hoc comparisons, and the approach
by Coalition seems good, but it'd be nice to do a proper deep-dive. There might be something to learn from this.
* Give a proper write-up for how it all works.




