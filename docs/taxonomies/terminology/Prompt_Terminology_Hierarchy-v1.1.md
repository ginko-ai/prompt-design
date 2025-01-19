# Prompt Terminology Hierarchy v1.1

## 1. Prompt (1.1)
   - An input to a Generative AI model used to guide its output
   - Can consist of text, image, sound, or other media
   - Usually contains some text component

   ### Prompt Template (1.1)
   - A function containing variables replaced by media to create a prompt
   - Used to construct consistent prompting patterns

   ### Prompting (1.2.2)
   - Process of providing input to guide Generative AI output
   - Core interaction method with modern language models

      #### Context (1.2.1)
      - Additional information included in prompt
      - Provides background or constraints for the model

      #### Context Window (A.2.1)
      - Maximum token length model can process
      - Defines limit for combined prompt and response

      #### Priming (A.2.1)
      - Initial instructions that set behavior for subsequent interaction
      - Often includes role or behavioral guidelines

      #### Prompting Technique (1.2.2)
      - Blueprint for structuring prompts or prompt sequences
      - May include conditional logic or architectural patterns

         ##### In-Context Learning (2.2.1)
         - Learning from examples within prompt without weight updates
         - Uses exemplars and/or instructions to guide behavior

            ###### Few-Shot Prompt (2.2.1)
            - Includes multiple examples demonstrating desired behavior
            - Typically 2-100 examples depending on context length

            ###### Exemplar (1.2.2)
            - Individual examples showing task completion
            - Used to demonstrate patterns model should follow

         ##### Zero-Shot Prompt (2.2.1.3)
         - No examples provided, only instructions
         - Tests model's direct task understanding

      #### Orthogonal Prompt Types (A.2.4)
      - Different dimensions for categorizing prompts

         ##### Density (A.2.4.2)
         - Categorization based on token representation

            ###### Continuous Prompt (A.2.4.2)
            - Contains tokens not corresponding to vocabulary words
            - Used in soft prompting approaches

            ###### Discrete Prompt (A.2.4.2)
            - Only uses tokens from model's vocabulary
            - Standard approach for most applications

         ##### Originator (A.2.4.1)
         - Source/creator of the prompt

            ###### User Prompt (A.2.4.1)
            - Input provided by human user
            - Main interface for interaction

            ###### System Prompt (A.2.4.1)
            - High-level instructions setting model behavior
            - Often hidden from user

            ###### Assistant Prompt (A.2.4.1)
            - Model's own output used as subsequent input
            - Used in conversation chains

         ##### Prediction Style (A.2.4.3)
         - How model generates predictions

            ###### Prefix (A.2.4.3)
            - Predicts tokens after prompt
            - Common in modern autoregressive models

            ###### Cloze (A.2.4.3)
            - Fills in masked tokens within prompt
            - Used in BERT-style models

      #### Prompt Chain (1.2.2)
      - Sequence of prompts where outputs feed into subsequent prompts
      - Enables complex multi-step reasoning

   ### Prompt Engineering (1.2.2)
   - Iterative process of developing and refining prompts
   - Focuses on improving effectiveness for specific tasks

      #### Prompt Engineering Technique (1.2.2)
      - Specific strategies for prompt improvement
      - Can be manual or automated

      #### Meta-Prompting (2.4)
      - Using prompts to generate or improve other prompts
      - Recursive prompt optimization

      #### Answer Engineering (2.5)
      - Process of extracting and formatting model outputs

         ##### Verbalizer (2.5.3)
         - Maps model outputs to standardized labels
         - Ensures consistent interpretation

         ##### Extractor (2.5.3)
         - Rules for pulling specific information from responses
         - Often uses regex or structured parsing

         ##### Answer Trigger (2.5.3)
         - Specific phrases that signal relevant output
         - Used to identify key information

      #### Conversational Prompt Engineering (A.2.2)
      - Refining prompts through interactive dialogue
      - Real-time prompt adjustment

   ### Fine-Tuning (A.2.3)
   - Updating model weights for specific tasks

      #### Prompt-Based Learning (A.2.3)
      - Learning approaches centered on prompt optimization
      - Bridges prompting and traditional fine-tuning

      #### Prompt Tuning (A.2.3)
      - Direct optimization of prompt parameters
      - Keeps base model frozen while updating prompt