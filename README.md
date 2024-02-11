<p align="center">
<img src="theme/assets/image.png" height="200">
<br>
<img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue">
</p>

### `CadenceAI`: Your all-in-one AI-powered cycling coach, mechanic, analyst and dietitian 🚴🏻‍♀🤖️🚴‍♂
Did you know there are over 1 billion bicycles in the world? The cycling industry is entirely commoditised.
However, **helpful** and **personalised** advice on training, repair and nutrition is out of reach for most people. 

Introducing - `Cadence AI`, your all-in-one AI-powered cycling coach, mechanic, analyst and dietitian. 


# MVP1

## Features in progress
- [ ] Anvil BE <-> FE pretty form app with text submission and response display 
- [ ] BE: Deploy Zephyr into public Cloud Run instance with auth
- [ ] Feature 1: General Q&A ("How of often should I change my chain?")
- [ ] FE: Deploy Anvil app to Compute Engine 
- [ ] Test e2e mobile usability and get early feedback   
- [ ] Multimodality (GeminiPro Vision API call) Bike component identifier (helps during repairs: "What is this part? [insert image] Oh, it's called bottom bracket!")

<p align="center">
<img src="docs/img/mvp1.png">
</p>

# Contact 
You can contact me for collaborations ideas at https://glukicov.github.io/

# MVP2+ features backlog and ideas 
- [ ] Price estimation ("How much would a new chain cost for my bike?")
  - [ ] Use LangChain/agents to retrieve and show online products
- [ ] Fine-tune the OSS LMM model (improve general Q&A) 
- [ ] Use RAG with a database of common cycling questions and answers
- [ ] Caching for recently answered questions (consider safety)
- [ ] Defensive UX
- [ ] Analyse historical trends in my cycling data ("Plot of average cadence per week over the last year")
  - [ ] Use Strava API to retrieve athlete's data (one-off)
- [ ] Dashboards with all trends
  - [ ] Sync with athlete's Strava (can be a manual push/analyse request for now) 
- [ ] Cycling coach to suggest exercises to improve the trends
- [ ] Dietitian to suggest nutrition plans 
- [ ] Recommend components to upgrade or buy 
  - [ ] Add athlete's bike into profile    

# Engineering backlog
- [ ] Add [Pkl](https://pkl-lang.org/blog/introducing-pkl.html) for config validation
- [ ] CI/CD for deployment and testing