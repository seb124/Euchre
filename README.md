# Euchre

This is an interactive, text-based version of the card game Euchre. https://bicyclecards.com/how-to-play/euchre/
The human user is player 1, on a team with player 3 against the other 2 plays. Cards used are 9 -> Ace ascending.
The goal is to win more tricks than the other team. The first team to 11 points win.

Install all required packages using conda and the `environment.yml` file.

To use the AISmack class, download LM Studio, then download the model `Llama 3.2 IB Instruct 4bit` within LM Studio.
Then, start a server on port 1234 using LM Studio and load the downloaded model. The AISmack class should now function. 

To play the game, type `python main.py`. To change which AI version is playing, edit the `config.json` file with the appropriate version name.