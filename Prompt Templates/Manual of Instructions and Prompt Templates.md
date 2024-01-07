<div align="center">
  <h3>Filomena's Manual of Instructions and Prompt Templates</h3>
  <h1> Leveraging Filomena's Potencial</h1>
  
<p><em> The present document aims to showcase the most appropriate approaches to obtain optimal outputs from the ChatBot Filomena. It highlights guidelines and examples of what to do and what prompts to avoid. </em></p>


</div>



![Filomena](https://cdn.discordapp.com/attachments/1150843302644547768/1190661589347602492/1000_F_378272550_xN8H7ZVudgCYWzfuZxRxVS5uFKjzsoMg.jpg?ex=65a29d04&is=65902804&hm=4a84c24f579a1d8ac5493b28f47b50c1dc7aaabc2832cb090bd7e4e95b2ab786&)

## Motivation

As a group, and being this our first interaction with implementing and leveraging LLM's to build a virtual assistant, we acknowledge that Filomena may have some flaws, and that - as occurs for the all LLM's - producing quality prompts yields a higher possibility of having better responses.

For this reason, we considered appropriate to define a manual of guidelines to interact with the ChatBot, such that the user is able to have all their queries satisfied in a timely and efficient manner.


## Guidelines

### General


1.  In certain cases, such as producing restaurant recommendations, Filomena can become a bit slow to deliver their response. In this case, patience is key.
2.  When querying Filomena, the prompt should be concise and direct.
3. The language may be either casual or formal, but slang should be avoided.
4.  The prompts should not be vague, but rather clearly explain the question being considered. Avoid ambiguity to make the responses more focused.
5.  Make only one request per prompt. For example, instead of making two questions in one prompt, use one prompt per question. 
6.  Ensure there are no misspellings in your request.
7.  If the initial response is not perfect, ask follow-up questions or rephrase your input for better results.
8.  FlavourFlix has a conversation history. To maintain a coherent conversation, reference those previous messages. If you're continuing a topic, briefly summarize the context to ensure Filomena understands the ongoing discussion. This helps create a more natural and context-aware interaction.
9.  Refine your queries based on the model's responses. Ask for clarification or provide more details to guide the model toward the desired outcome.
10.  Experiment with different phrasings and approaches if the initial response is not satisfactory. Iterative conversations often lead to improved results.
11.  Filomena is not built to answer questions about themeses besides FlavourFlix context and portuguese gastronomy. Thus, anything that is distant from this scope may be completely innacurate.


### Questioning Based on Documents Retrieval

1. Specify what you are looking for with keywords directly linked to FlavourFlix.
2. Do not ask for things unrelated with FlavourFlix or the Portuguese gastronomic culture.
3. Use short and clear sentences.
4. Avoid making multiple questions in the same prompt.

__Keyword Examples__

``` 
FlavourFlix; Food Personality; Founders of FlavourFlix; Analytics Dashboard; Current Location Feature; Portugal; ...;
````

### Requesting Restaurant Descriptions

1. Clearly state that you are looking for the description of a given restaurant.
2. Indicate clearly the name of the restaurant you are looking for, ensuring it is complete and correct.
3. In order to avoid confusing restaurant's names with people's names (e.g: "O Marinho"), identify that you are looking for a restaurant.
4. Writing down the name wrongly may result in errors. 

### Asking for Restaurant Recommendations

1. At first, state that you are looking specifically for a restaurant recommendation.
2. Filomena will then afterwards prompt you to indicate what exactly you are looking for, namely the location you desire, your food personality and other dining preferences.
3. Provide these inputs in a clear and concise manner such that it is quicker for Filomena to process them. 
4. The inputs should be provided all within the same prompt.
5. Filomena will now get you a recommendation, if the prior steps were sucessfull.
6. If you are not pleased with your restaurant recommendation, state that you are looking for a new restaurant recommendation and repeat the steps.

### Uncovering your Food Personality

1. At first, state that you want to know your Food Personality.
2. If Filomena already has access to this variable (e.g: you have already taken the Food Personality quiz directly in the app), she will describe to you your Food Personality prediction. Otherwise, she will prompt you to answer a the questions of the quiz.
3. Answer the questions correctly and clearly, by expressing your answers on a scale from 1 (**Strongly Disagree**) to 5 (**Strongly Agree**). It is best to make your answers in the same order the questions appear in, OR, write down the question and the respective answer in front.
4. Ensure the answers to the quiz are all answered simultaneously in the same request.
5. If these steps were sucessful, Filomena will predict your personality type and describe it.

   
## Prompt Examples - Do's & Dont's

### Questioning Based on Documents Retrieval
__Guideline 1.__

```
DO: "What are the FlavourFlix food personalities?"
DO NOT: "What is my personality?"
```

__Guideline 2.__
```
DO: "Describe me portuguese festivities?"
DO NOT: "Who wrote the song 'Thriller'?"
```

__Guideline 3.__
```
DO: "Tell me more about FlavourFlix app features?"
DO NOT: "Tell me more about the FlavourFlix features what they can do how were they created what is behind them?"
```

__Guideline 4.__ 
```
DO: "Describe the roles of the founders of FlavourFlix."
DO NOT: "Tell me who are the founders of FlavourFlix and describe their roles."
```

### Requesting Restaurant Descriptions

__Example Prompt (Illustrates all Guidelines)__
```
DO: "I want to know more about the restaurant 'Chutneys'."
DO NOT: "Tell me about Marinho."
```

### Asking for Restaurant Recommendations

__STEP 1.__
```
DO: "I want a restaurant recommendation, please."
DO NOT: "Recommend me a restaurant in Lisbon that serves pizza."
```

__STEP 2.__
```
DO: "The restaurant must be in Lisbon. My food personality is 'Comfort Food Lover'".
DO NOT: "I want a restaurant that will make me feel good."
```

__STEP 3.__
```
DO: "I did not like it. Please provide me with another restaurant recommendation."
DO NOT: "I don't like it."
```
### Uncovering your Food Personality

__STEP 1.__
```
DO: "I want to know more about my food personality, please."
DO NOT: "What is my food personality? Can you explain the food personalities?"
```

__STEP 2.__
Answering the questionnaire:
```
DO: "How open are you to trying unfamiliar and exotic dishes? Answer:2, How important is the presentation and plating of your food? Answer:4, (...)"
DO NOT: "I think it's 0"
```

__STEP 3.__
```
DO: "I want to know more about the food personality "Confort Food Lover""
DO NOT: "What is Food Lover?"
```
