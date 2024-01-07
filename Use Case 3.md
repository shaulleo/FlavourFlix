<div align="center">
  <h3>USE CASE 3</h3>
  <h1> COMBINE MACHINE LEARNING WITH FOOD </h1>
<p><em> Ever wondered how to describe in three words your patterns and trends within food and dining experiences? Filomena has got you covered! </em></p>
</div>

![Placeholder Image](ext_images\personalities\fine_dining_connoisseur.png)

## Description

Not only Filomena can respond to your questions, she can also determine your personality type through a questionnaire.  There are several possibilities, a user can have an Adventurer personality, or be a Fine Dining Connoisseur, Low Cost Foodie, Comfort Food Lover or even a Conscious Eater. 

This process is enabled by integrating a Machine Learning classifier within a LLM agent such that, based on a query of the user responding to the provided questionnaire, Filomena is able to categorize the inputs and retrieve the user's personality. 


## Examples 

<div align="center">
  <img src="ext_images\personality fil 1.png" alt="Filomena finds your personality 1" style="width: 49%;">
  <img src="ext_images\personality fil 2.png" alt="Filomena finds your personality 2" style="width: 
  49%;">

</div>



## Personality Description

- __The Adventurer__:  Enjoys trying new, exotic, and often challenging foods. Prefers variety and
unique culinary experiences over comfort foods.

- __Fine Dining Connoisseur__: Appreciates high-end, gourmet food. Values presentation, quality
of ingredients, and the overall dining experience in upscale environments.

- __Low Cost Foodie__: Enjoys finding delicious food at a bargain. Values taste and affordability over ambiance and presentation.
- __Conscious Eater__: Prioritizes nutritional value and health benefits, with a strong focus on
	vegetarian and vegan choices.
- __Comfort Food Lover__: Prefers traditional, home-cooked, or familiar dishes. Values the
emotional connection and nostalgia associated with food.

## Prompt Templates and Instructions

To maximize Filomena's potential when answering your questions, please refer to the [Filomena's Instructions Documentation](https://github.com/shaulleo/FlavourFlix/blob/main/Prompt%20Templates/Manual%20of%20Instructions%20and%20Prompt%20Templates.md) and follow the guidelines and prompt templates presented there.

## Actors

- FlavourFlix' user, who wants to learn more about a specific restaurant.
- Filomena, FlavourFlix' assistant.

### Preconditions
- The Bot is seamlessly integrated into the FlavourFlix application and running smoothly.
- Users have logged in and gained access to the "Chat with Filomena" interface.

### Main Flow
1. __User's Introduction__:
    
The FlavourFlix User initiates contact with Filomena when entering the "Chat with Filomena" interface.

2. __Filomena's Greeting__:
    
Filomena welcomes the User and asks the user in what she may assist them.

3. __User's Interest in Personality__:

The User presents interest in learning about their food personality type.

4. __Filomena's Performs the Questionnaire__:
 
Filomena asks for the user to answer to a questionnaire with 10 queries on a scale from 1 to 5, whereas 1 represents *"Strongly Disagree"* and 5 represents *"Strongly Agree"*.

5. __User's Reflection__:

The User responds to Filomena's questionnaire in the required format.

6. __Filomena Uncovers the User's Personality__:

If the inputs are correctly presented and the user responds to all of the questions, Filomena is able to use the Classifier and uncover the Food Personality of the user.

### Alternative Flows
1. __Feeding the Wrong or Misunderstanding of Inputs__:

If Filomena is not able to grasp the User's questionnaire responses or the user was not able to provide all the answers, Filomena states that she was not possible to complete the request and recommends the user to perform the questionnaire directly in the app.

