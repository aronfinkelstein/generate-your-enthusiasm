'''
Splitting the data into:
- manually labelled set
- training set
- validation set
- testing set
'''
import json
import random
import re
from pathlib import Path

def split_into_sentences(text):
    """Split text into sentences by period followed by whitespace or space mark.
    Handles common abbreviations and edge cases."""
    
    # Common abbreviations to ignore
    abbreviations = {'mr.', 'mrs.', 'ms.', 'dr.', 'prof.', 'sr.', 'jr.', 'vs.', 
                    'i.e.', 'e.g.', 'etc.', 'fig.', 'vol.', 'rev.', 'no.'}
    
    text_lower = text.lower()
    potential_sentences = []
    start = 0
    
    for i in range(len(text)):
        if text[i] == '.' and (i + 1 == len(text) or text[i + 1].isspace()):
            # Check if period is part of an abbreviation
            word_end = text_lower[max(0, start-20):i+1].strip()
            is_abbreviation = any(word_end.endswith(abbr) for abbr in abbreviations)
            
            if not is_abbreviation:
                potential_sentences.append(text[start:i+1].strip())
                start = i + 1
    
    # Add any remaining text
    if start < len(text):
        potential_sentences.append(text[start:].strip())
    
    return [s for s in potential_sentences if s.strip()]

def get_word_count(text):
    return len(text.split())

def sample_sentences_from_episodes(sentences, max_sentences):
    """Sample sentences while maintaining episode context and not exceeding max_sentences."""
    if len(sentences) <= max_sentences:
        return sentences
    
    # Group sentences by episode
    episodes = {}
    for sent in sentences:
        ep_id = sent['episode_id']
        if ep_id not in episodes:
            episodes[ep_id] = []
        episodes[ep_id].append(sent)
    
    # Calculate how many sentences to take per episode
    sentences_per_episode = max(1, max_sentences // len(episodes))
    
    sampled_sentences = []
    for ep_sentences in episodes.values():
        sampled = random.sample(ep_sentences, min(sentences_per_episode, len(ep_sentences)))
        sampled_sentences.extend(sampled)
    
    # If we still need more sentences, randomly sample from remaining
    if len(sampled_sentences) < max_sentences:
        remaining = [s for s in sentences if s not in sampled_sentences]
        additional = random.sample(remaining, min(max_sentences - len(sampled_sentences), len(remaining)))
        sampled_sentences.extend(additional)
    
    # If we have too many sentences, randomly remove some
    if len(sampled_sentences) > max_sentences:
        sampled_sentences = random.sample(sampled_sentences, max_sentences)
    
    return sampled_sentences

def split_dataset(input_file, output_dir, max_manual_sentences=100):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Process IMDB and Wikipedia synopses into sentences
    imdb_sentences = []
    wiki_sentences = []
    
    for episode_id, episode_data in data.items():
        if 'imdb_synopsis' in episode_data and episode_data['imdb_synopsis'].strip():
            sentences = split_into_sentences(episode_data['imdb_synopsis'])
            for sentence in sentences:
                if len(sentence.split()) > 3:
                    imdb_sentences.append({
                        'episode_id': episode_id,
                        'source': 'imdb',
                        'text': sentence,
                        'season': episode_data.get('season', 'unknown'),
                        'episode': episode_data.get('episode', 'unknown'),
                        'word_count': get_word_count(sentence)
                    })
                    
        if 'wikipedia_synopsis' in episode_data and episode_data['wikipedia_synopsis'].strip():
            sentences = split_into_sentences(episode_data['wikipedia_synopsis'])
            for sentence in sentences:
                if len(sentence.split()) > 3:
                    wiki_sentences.append({
                        'episode_id': episode_id,
                        'source': 'wikipedia',
                        'text': sentence,
                        'season': episode_data.get('season', 'unknown'),
                        'episode': episode_data.get('episode', 'unknown'),
                        'word_count': get_word_count(sentence)
                    })
    
    # Sample sentences for manual set (50-50 split between sources)
    manual_imdb = sample_sentences_from_episodes(imdb_sentences, max_manual_sentences // 2)
    manual_wiki = sample_sentences_from_episodes(wiki_sentences, max_manual_sentences // 2)
    manual_set = manual_imdb + manual_wiki
    
    # Get episode IDs in manual set
    manual_episode_ids = set(s['episode_id'] for s in manual_set)
    
    # All remaining sentences go to auto-label set
    auto_label_imdb = [s for s in imdb_sentences if s['episode_id'] not in manual_episode_ids]
    auto_label_wiki = [s for s in wiki_sentences if s['episode_id'] not in manual_episode_ids]
    auto_label_set = auto_label_imdb + auto_label_wiki
    
    datasets = {
        'manual': manual_set,
        'auto_label': auto_label_set
    }
    
    # Save and print statistics
    for name, dataset in datasets.items():
        output_file = output_dir / f'{name}_set.json'
        with open(output_file, 'w') as f:
            json.dump(dataset, f, indent=2)
        
        imdb_count = sum(1 for s in dataset if s['source'] == 'imdb')
        wiki_count = sum(1 for s in dataset if s['source'] == 'wikipedia')
        avg_word_count = sum(s['word_count'] for s in dataset) / len(dataset) if dataset else 0
        
        print(f'\n{name.capitalize()} Set Statistics:')
        print(f'Total sentences: {len(dataset)}')
        print(f'IMDB sentences: {imdb_count}')
        print(f'Wiki sentences: {wiki_count}')
        print(f'Average sentence length: {avg_word_count:.1f} words')
        print(f'Unique episodes: {len(set(s["episode_id"] for s in dataset))}')

if __name__ == "__main__":
    input_file = Path(__file__).parents[2] / "backend/data/clean_curbdata.json"
    output_dir = Path(__file__).parents[2] / "backend/data/split_data_sentences"
    split_dataset(input_file, output_dir)