# Plan For G-Y-E

The overall aim for this project is to train a model to predict curb your enthusiasm plots based on specific user inputs. Data to train the model is imdb and wikipedia plot synopses.

## Overall Plan (Back-End)

### Data Collection

- [x] Find useful data sources
- [x] Web scrape or use API to collect data
- [x] Format Data in useful structure (Json probably)

### Data Preprocessing and Labelling

- [ ] Clean text data
- [ ] Tokenize and normalize the text

- [ ] Split data into training, validation, and test sets.
- [ ] Develop a schema for manual labelling based on the spacy labelling schema
- [ ] Manually label a subset of training data.
- [ ] Create a set of heuristics or weak supervision rules to auto-label the rest of the data.
- [ ] Refine the labelling process iteratively to improve accuracy.

- [ ] Train a custom SpaCy Named Entity Recognition (NER) model to extract characters, locations, and comedic elements.
- [ ] Evaluate the SpaCy model and refine based on results.

### Training language model

Model Selection:

- [ ] Evaluate different pre-trained language models (e.g., BERT, GPT).
- [ ] Choose the most appropriate model

Training:

- [ ] Fine-tune the selected model on the labelled dataset.
- [ ] Experiment with hyperparameters to optimize model performance.
- [ ] Use validation data to evaluate model during training.

Improvements:

- [ ] Analyze error cases to identify weaknesses in the model.
- [ ] Fine-tune or retrain the model as needed.

### Extra Framework

- [ ] Build a pipeline to preprocess user inputs before feeding them into the model.
- [ ] Integrate the trained language model for generating outputs.
- [ ] Post-process model outputs to ensure coherence and relevance to Curb Your Enthusiasm style.
- [ ] Test the system end-to-end with sample inputs.
