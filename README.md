## Riot Policy

Please note that my project is not endorsed by Riot Games and does not reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties. Riot Games and all associated properties are trademarks or registered trademarks of Riot Games, Inc.

## Overview
League of Legends ("LoL") is a popular multiplayer online battle arena (MOBA) video game developed and published by Riot Games. With millions of players worldwide, it has become a competitive eSports phenomenon. Two teams of five players play against each other to destroy the opposing team's Nexus, which is guarded by the enemy champions and defensive structures. Each team's Nexus is located in their base, where players start the game and respawn upon death. Non-player characters, the minions, are generated from each team's Nexus and advance towards the enemy Nexus along the three lanes, where it contains the three "inhibitors. Destroying an inhibitor spawns a super minions in that lane, and allows the attacking team to damage the enemy Nexus and the last two guard turrets. The regions in between the lanes are collectively known as the "jungle", with neutral monsters that respawn at regular intervals. Most importantly, powerful monsters spawn in each side of the river, where killing the monster grant special abilities to the slayers' team. For example, teams can gain a powerful allied unit after killing the Rift Herald, permanent strength boosts by killing dragons, and/or, a strong buff that enhances the allied minions by killing the Baron Nashor.

<p align="center">
  <img src="https://raw.githubusercontent.com/sanghoonmaeng/league_of_legend_prediction/master/Summoner-Rift-Map.webp" alt="League of Legends Game Map" width="800" height="450">
</p>

This project aims to enhancing the League of Legends experience by developing a predictive model that helps players to anticipate the outcome of ranked matches. By leveraging machine learning techniques and game data analysis, we aim to provide valuable insights to players looking to improve their win rates and climb the ranked ladder.

## Data Collection
League of Legends matches is available to developers through the [Riot Games API](https://developer.riotgames.com/docs/lol). After registering for a development API key with rate limits of 20 requests every 1 seconds(s) and 100 requests every 2 minutes(s), I created a python script to collect, extract, clean, and preprocess 10,000 Master's ranked match data for the prediction models. 

## Model Training
A simple neural network, random forest, and XGBoost models were trained with tuned hyperparameters.

## Result
All three models achieved relatively high accuracy, precision, and recall. As expected, the XGBoost model had the best performance and destroying the first inhibitor had the most influence in winning the game.

## Comment
Unfortunately, Riot API does not provide live match data to keep the integrity of the game, and the spectator mode API request returns a completely different data. Consequently, our current predictive capabilities do not extend to real-time match outcomes, but however, we might be able to apply our prediction model on LoL eSports world championship game, where the applicable features are displayed on live. 

## Image Source
[Summoner's Rift Map](https://riftfeed.gg/guides/league-of-legends-maps-a-fundamental-guide)
