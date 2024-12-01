import json
from pathlib import Path
import spacy
from spacy.tokens import DocBin
from spacy.training import Example
import random
from collections import defaultdict

def extract_entities_from_text(text, nlp):
    """Extract entities from text using current model to create training data"""
    doc = nlp(text)
    entities = [(ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]
    return entities

def create_training_data(file_path, base_model="en_core_web_sm"):
    """Create training data from actual entities in episodes"""
    nlp = spacy.load(base_model)
    
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    training_data = []
    entity_counts = defaultdict(set)  # Track unique entities by type
    
    for episode_id, episode_data in data.items():
        # Get both synopses
        imdb_text = episode_data.get('imdb_synopsis', '')
        wiki_text = episode_data.get('wikipedia_synopsis', '')
        
        # Process each synopsis separately to maintain proper character positions
        for text in [imdb_text, wiki_text]:
            if not text.strip():
                continue
                
            # Get entities from current model
            entities = extract_entities_from_text(text, nlp)
            
            # Add to training data
            if entities:
                # Track unique entities
                for _, ent_text, label in entities:
                    entity_counts[label].add(text[entities[0]:entities[1]])
                
                training_data.append((text, {"entities": entities}))
    
    # Print statistics about found entities
    print("\nEntity Statistics:")
    for label, entities in entity_counts.items():
        print(f"{label}: {len(entities)} unique entities")
    
    return training_data

def train_ner_model(training_data, output_dir, n_iter=30):
    """Train the NER model with the extracted entities"""
    nlp = spacy.load("en_core_web_sm")
    
    # Create or get the NER pipe
    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner")
    optimizer = nlp.create_optimizer()
    
    # Get names of other pipes to disable during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    
    # Train the model
    with nlp.disable_pipes(*other_pipes):
        if "ner" in nlp.pipe_names:
            nlp.get_pipe("ner").initialize()
            
        print("Beginning training...")
        for itn in range(n_iter):
            random.shuffle(training_data)
            losses = {}
            batches = spacy.util.minibatch(training_data, size=8)
            
            for batch in batches:
                examples = []
                for text, annotations in batch:
                    doc = nlp.make_doc(text)
                    example = Example.from_dict(doc, annotations)
                    examples.append(example)
                
                nlp.update(examples, drop=0.2, losses=losses)
            
            print(f"Iteration {itn+1}/{n_iter}, Losses: {losses}")
    
    # Save the model
    if output_dir:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir(parents=True)
        nlp.to_disk(output_dir)
        print(f"Model saved to {output_dir}")
    
    return nlp

def evaluate_model(model, test_text):
    """Evaluate the model on a test case"""
    doc = model(test_text)
    print("\nModel Evaluation:")
    for ent in doc.ents:
        print(f"Entity: {ent.text:<20} Label: {ent.label_}")

def main():
    file_path = Path(__file__).parents[2] / "data" / "curbdata.json"
    output_dir = Path(__file__).parents[2] / "models" / "curb_ner"
    
    # Create training data from actual entities
    print("Extracting training data from episodes...")
    training_data = create_training_data(file_path)
    print(f"Created {len(training_data)} training examples")
    
    # Split into training and validation sets
    random.shuffle(training_data)
    split = int(len(training_data) * 0.9)  # 90% training, 10% validation
    train_data = training_data[:split]
    valid_data = training_data[split:]
    
    # Train the model
    trained_model = train_ner_model(train_data, output_dir)
    
    # Test the model
    test_texts = [
        "Larry David gets into an argument with Jeff Greene at a Palestinian restaurant.",
        "Cheryl convinces Larry to attend a fundraiser in Beverly Hills.",
        "Leon and Larry visit Richard Lewis at his new house in Hollywood."
    ]
    
    for text in test_texts:
        evaluate_model(trained_model, text)

if __name__ == "__main__":
    main()