# Generate Your Enthusiasm

As an engineering student, I am often told that I can use my new-found knowledge and technical expertise to help change the world for the better. This has always inspired in me a determination to push the boundaries of technology and help to nudge humanity forward into a utopian, post-scarcity future in which all struggles are a distant memory. I therefore naturally decided that a greater understanding of the HBO-series, Curb Your Enthusiasm, would contribute massively to this dream.

Penicillin was discovered accidentally, as were microwaves, x-rays, pace-makers. Even Play-Doh. Throughout this project I have been accutely aware that even the analysis of one episode, might lead to the discovery of a cure to a terminal illness or even a new childs toy. I haven't discovered either of those yet, but I also might have unknowingly, that's the trouble with trying to discover something accidentally I guess.

Anyway, I think it was Einstein or someone equally important, that wrote 'Larry David's writing is the key to humanities' greatest secrets and possibly the meaning of life' (I might be paraphrasing). I am astonished that this analysis has been left to an under-graduate student, clearly government research-funding needs to be reprioritised. Nonetheless, I have dedicated myself to this research entirely, possibly at the expense of my behaviour-of-dynamic-systems revision, but I am convinced that the humanitarian impact of this work will be worth the significant cost to my career prospects.

If only Mr. David would just reveal his secrets...

## Table of Contents

1. [Description](#generate-your-enthusiasm)
2. [Installation](#installation)
3. [How I Built This](#how-i-built-this)
4. [Features](#features)
5. [Development Process](#development-process)
6. [Roadmap](#roadmap)
7. [Contact Information](#contact-information)

## How I Built This

### Data Collection

In order to train the model, I considered various data types. Curb is an improvised show and therefore, scripts aren't actually available. I could have used transcripts or subtitles, but I couldn't find a source that had labelled scripts, just the transcription of speech. Instead, I decided to use the imdb and wikipedia synopsis for each episode as training data.

### Training an NER model

I decided to use the spaCy "en_core_web_sm" as a base model for this project, and worked on training the model to automatically label the synopses for later use. I split the data into different sets and cleaned it of unicode and html elements. I decided to manually label randomly selected sections of 20 synopses. I did this using label studio, and used the spaCy schema. There were a few decisions to be made, and the regualar definitions of people and products had to be slughtly altered to account for inside jokes and specific references within the show. For example the Shucker would usually not be labelled as a PERSON by spaCy, but for this project, it needed to be, he plays an important role.
