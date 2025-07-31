from datasets import load_dataset
# or load the separate splits if the dataset has train/validation/test splits
valid_dataset = load_dataset("asgaardlab/GameplayCaptions", split="validation")
