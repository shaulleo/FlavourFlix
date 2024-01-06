<div align="center">
  <h3>USE CASE 1</h3>
  <h1>LEVERAGING FILOMENA TO GAIN KNOWLEDGE</h1>
<p><em>Want to know a bit more about FlavourFlix but don't know where to start? With Filomena, there is no need for an interminable search.</em></p>

</div>


![Placeholder Image](link_to_image)

## Description

Filomena is a ChatBot with many functionalities - one of its main innovations is the fact that Filomena can aid the user in discovering more about FlavourFlix without them needing to directly search for it. In this context, Filomena is able to talk about the company's culture and value proposition, provide a business overview, and discuss its founder's background.

Moreover, despite talking about FlavourFlix, Filomena is also able to describe the functionalities of the web platform, such as describing the FlavourFlix food personalities, answer Frequently Asked Questions (FAQ), troubleshoot issues the user may find within the web app and, - finally but not least -, she can also present an overview of Portuguese gastronomic culture and present some fun facts about the typical cuisine of Portugal.

All of these possibilities are enabled by Filomena's capabilities of selecting relevant excerpts from a Vector Database containing embeddings of multiple text data files. These are selected through the keywords of the query provided, and may be found in the [Data Description](https://github.com/shaulleo/FlavourFlix/blob/main/Data%20Description.md).

## Summary of Topics Accepted
- Issues with FlavourFlix Platform.
- FlavourFlix Company Description and Overview.
- Information about FlavourFlix' Founders and Developers.
- Questions about the Platform Interface.
- Questions about FlavourFlix' Features.
- Trivia about Portugal's Gastronomic Culture.

## Examples 
![Example Image 1](example_image_1_link)
![Example Image 2](example_image_2_link)
![Example Image 3](example_image_3_link)

For more examples, refer to [this link](link_to_examples).

## Prompt Templates and Instructions

To maximize Filomena's potential when answering your questions, please refer to the [Filomena's Instructions Documentation](link_to_documentation) and follow the guidelines and prompt templates presented there.

## Actors

- FlavourFlix user interested in learning more with Filomena.
- Filomena, FlavourFlix' assistant.

### Preconditions
- The Bot is seamlessly integrated into the FlavourFlix application and running smoothly.
- Users have logged in and gained access to the "Chat with Filomena" interface.

### Main Flow
1. __User's Call to Adventure__:
    
The FlavourFlix User initiates contact with Filomena when entering the "Chat with Filomena" interface.

2. __Filomena's Greeting__:
    
Filomena welcomes the User and asks the user in what she may assist them.

3. __User's Query__:

The User poses a question to Filomena, seeking information about the topics mentioned.

4. __Filomena's Enigmatic Processing__:
 
Utilizing its document-retrieval algorithms and LLM's to process the queries, Filomena deciphers the User's intention and is able to correctly inform their queries.

5. __Continuous Questioning__:

The User may continue making questions to Filomena. She is able to answer based on a number of given prior messages.

### Alternative Flows
1. __Filomena's Misunderstanding__:

If Filomena is not able to grasp the User's query or find the appropriate answer, she states that she is not designed to answer that kind of question or does not have sufficient data to be able to provide an accurate response.
