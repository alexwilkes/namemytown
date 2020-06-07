# namemytown
How does this work?

New town names are built left-to-right using a Random Forests classifier that predicts the next letter based on the previous three letters. Within each iteration, it chooses the next letter from a probability distribution that is weighted by the votes of the Random Forest ensemble. As well as another letter, this process can also predict that the town name should terminate. Two separate models are trained for US cities and English cities.


What data was it trained on?

Data is scraped from the List of cities and towns in England wikipedia article, the list of cities and towns in Germany, the Britannica list of US towns and cities and Britannica list of cities and towns in France.


To do

- Cache scraped lists
- Make scraping approach more robust
- Vary the length of the feature vector beyond 3 preceeding characters
