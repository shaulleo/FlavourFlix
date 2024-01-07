<div align="center">
  <h3>USE CASE 2</h3>
  <h1> SATISFY CURIOUSITY AND GET TO KNOW YOUR NEIGHBOURING RESTAURANTS</h1>
<p><em> Do you know when you pass that specific restaurant on your way to work, and you always wonder what is it like? Filomena can give you a complete description of it! You only need to provide its name. </em></p>

</div>


![Image](FlavourFlix/ext_images/pexels-cátia-matos-984888.jpg)

## Description

The virtual assistant Filomena comprises a wide range of features. Namely, she provides with the possibility of getting to know a restaurant without ever leaving the house, by gathering a synthetic but rather complete description of the restaurant, including information about their average prices, cuisine types, restaurant style and much more.

This is possibilited by Filomena's ability of extracting the restaurant's name from the user input, preprocessing it, and sending it to an agent which performs a search operation of the restaurant within FlavourFlix' restaurant database. The latter may be found in the [Data Description](https://github.com/shaulleo/FlavourFlix/blob/main/Data%20Description.md).

## Examples 
![Example Image 1](example_image_1_link)
![Example Image 2](example_image_2_link)
![Example Image 3](example_image_3_link)

For more examples, refer to [this link](link_to_examples).

## Prompt Templates and Instructions

To maximize Filomena's potential when answering your questions, please refer to the [Filomena's Instructions Documentation](link_to_documentation) and follow the guidelines and prompt templates presented there.

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

3. __User's Display of Curiosity__:

The User presents interest in learning more about a given restaurant.

4. __Filomena's Enigmatic Processing__:
 
Filomena is able to portray information about the restaurant by preprocessing the user input and sending an agent to search for the restaurant name found in the input within the restaurant database.

5. __Continuous Questioning__:

The User may continue making interacting with Filomena, even change topics. She is able to answer based on a number of given prior messages.

### Alternative Flows
1. __Filomena's Misunderstanding__:

If Filomena is not able to grasp the User's query or find the appropriate answer, she states that she is not designed to answer that kind of question or does not have sufficient data to be able to provide an accurate response.
