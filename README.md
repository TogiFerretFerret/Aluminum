# Aluminum
This currently is PRIVATE as we are adding Cryptolens licensingm, and its on AZURE so.... yah.
## NOTE: Currently incompatible with Firefox due to Google Auth Proxying failing to capture the required blackbaud state token from the iframe in Firefox due to security something. A patch is coming soon. See issue [https://github.com/TogiFerretFerret/Aluminum/issues/6]
## If some moron is using firefox on public istg....
luckily firefox is banned on school comps lol.
## NOTE: Please ignore @DarkSystemGit's issues. His one requirement for working on this was I let him put at least 1 bullshit issue, but he's important cuz I hate nodejs.
An explosively awesome desktop/mobile frontend for Blackbaud, built off the Bromine API.
basically whole thing has been reworked to be better at using azure so now its better and supports multi-user with minimal server load, so that's cool. also like cryptolens licensing is chill fr.
I would highly recommend using python 3.10 (atl i used that in testing).

run make uv and in another terminal tab run python3 lms.py

Edit makefile as necessary
### FAQ
#### How to install?
Get python (3.10 should work)
Install requirements (requirements.txt)
### IFAQ (Infrequently Frequently Asked Questions)
#### Why?
Since Blackbaud is dogshit
#### Why not just use the website?
Because the website is dogshit
#### Why not just use the app?
There is no app
#### Why not just use the mobile website?
Because the mobile website is dogshit
#### Why not just use the desktop website?
Because the desktop website is dogshit. I said that already.
#### Why not just use Gavin's Extension?
Gavin's Extension isn't bad, but it's kinda hacky. Mine is also kinda hacky, but it's a different kind of hacky.
#### Why not windows yet?
Yeah, it works on windows. There's litearlly a bat file right there. Moron.
#### Why is there two programming languages?
Basically, I didn't want to rewrite Ultraviolet (the proxy used for Google Authentication) when I made this, so uhh, have fun! And I wasn't going to write the rest of the app in JS, though DarkSystemGit (if he isn't working on Atto-24) should be responsible for the JS framework (still private, part of the Bromine Initiative (i havent even added all the api endpoints in this repo to it yet)
#### Why is the googleauth.py absolute garbage
I'll fix it eventually. It had to do with me debugging. It's less bad now.
like its gone now actually, i integrated it during the azure catastrophy of right fuckin' now.

why no tests is because i lazy and how da fuck u test this tho?
also yes mobile support is fukked i think cuz like something with ultraviolet, ill try to figure out why eventually maybe if I do itll probably just be a mobile app that uses like, just the raw api and written in a bunch of shitty swift code and a kitbash of react in there too since the backend is all fukky.
honestly i should just build out a good api endpoint and run with that but im lazy and dont want to.
honestly half the difficulty of this project is nonexistent because of how good ultraviolet is and the API RE isn't even hard, i already did discussion boards just too fucking lazy to implement a good ui for them and don't want to fuck up the RTE formatting.
also im probably gonna have to optimize most of the code since its all fucky rn and i really hate having to re-enter the key each time i feel like it makes people not wanna use it but the cookie will probably save their ass on that since they don't have to re-enter as long as cookie is like "valid".


if something fucks up, send an issue. I'll get to it when I can.
maybe. (probably though, I want to make this polished.)
