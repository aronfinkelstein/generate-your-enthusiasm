import json
from pathlib import Path
import spacy
from spacy.training import Example
import random
from collections import defaultdict

def create_training_data(file_path, base_model="en_core_web_sm"):
    """Create training data from actual entities in episodes"""
    nlp = spacy.load(base_model)
    
    # Add entity ruler for key characters and locations
    ruler = nlp.add_pipe("entity_ruler", before="ner")
    patterns = [
        {"label": "PERSON", "pattern": "Larry David"},
        {"label": "PERSON", "pattern": "Larry"},
        {"label": "PERSON", "pattern": "Jeff Greene"},
        {"label": "PERSON", "pattern": "Cheryl"},
        {"label": "PERSON", "pattern": "Leon Black"},
        {"label": "PERSON", "pattern": "Richard Lewis"},
        {"label": "PERSON", "pattern": "Ted Danson"},
        {"label": "PERSON", "pattern": "Susie Greene"},
        {"label": "GPE", "pattern": "Los Angeles"},
        {"label": "GPE", "pattern": "Beverly Hills"},
        {"label": "ORG", "pattern": "HBO"}
    ]
    ruler.add_patterns(patterns)
    
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    training_data = []
    entity_counts = defaultdict(set)
    
    for episode_id, episode_data in data.items():
        # Process both synopses
        for source in ['imdb_synopsis', 'wikipedia_synopsis']:
            text = episode_data.get(source, '')
            if not text.strip():
                continue
                
            doc = nlp(text)
            entities = []
            
            # Filter and validate entities
            for ent in doc.ents:
                # Skip likely wrong classifications
                if (ent.label_ in ['GPE', 'ORG', 'LOC'] and 
                    ent.text in ['Larry', 'Julia', 'Cheryl', 'Jeff']):
                    continue
                    
                entities.append((ent.start_char, ent.end_char, ent.label_))
                entity_counts[ent.label_].add(ent.text)
            
            if entities:
                training_data.append((text, {"entities": entities}))
    
    # Print entity statistics
    print("\nEntity Statistics:")
    for label, entities in entity_counts.items():
        print(f"\n{label}: {len(entities)} unique entities")
        print("Sample entities:", sorted(list(entities))[:5])
    
    return training_data

def train_ner_model(training_data, output_dir, n_iter=30):
    """Train the NER model with the extracted entities"""
    nlp = spacy.load("en_core_web_sm")
    
    # Add entity ruler
    if "entity_ruler" not in nlp.pipe_names:
        ruler = nlp.add_pipe("entity_ruler", before="ner")
    
    # Initialize labels for the NER
    ner = nlp.get_pipe("ner")
    
    # Get all labels from training data
    labels = set()
    for _, annotations in training_data:
        for _, _, label in annotations.get("entities", []):
            labels.add(label)
    
    # Add labels to the NER
    for label in labels:
        ner.add_label(label)
    
    # Get names of other pipes to disable during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in ["ner", "entity_ruler"]]
    
    # Train the model
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.initialize()
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

def main():
    file_path = Path(__file__).parents[2] / "data" / "curbdata.json"
    output_dir = Path(__file__).parents[2] / "models" / "curb_ner"
    
    print("Extracting training data from episodes...")
    training_data = create_training_data(file_path)
    print(f"\nCreated {len(training_data)} training examples")
    
    # Train the model
    trained_model = train_ner_model(training_data, output_dir)
    
    # Test the model
    test_texts = [
        "Larry David gets into an argument with Jeff Greene at a Palestinian restaurant.",
        "Cheryl convinces Larry to attend a fundraiser in Beverly Hills.",
        "Leon and Larry visit Richard Lewis at his new house in Hollywood."
    ]
    
    print("\nTesting model on sample texts:")
    for text in test_texts:
        doc = trained_model(text)
        print(f"\nText: {text}")
        for ent in doc.ents:
            print(f"Entity: {ent.text:<20} Label: {ent.label_}")

if __name__ == "__main__":
    main()
