#!/usr/bin/env python3
"""
Secure Password Generator
Author: Olaoluwa Aminu-Taiwo
Description: Generates cryptographically secure passwords
"""

import random
import string
import secrets  # More secure than random for passwords

class PasswordGenerator:
	"""Generate secure passwords with custom requirements"""
	
	def __init__(self):
		self.lowercase = string.ascii_lowercase
		self.uppercase = string.ascii_uppercase
		self.digits = string.digits
		self.symbols = string.punctuation
		
		# Exclude ambiguous characters by default
		self.ambiguous = 'il1Lo0O'

	def generate(self,
				length: int = 16,
				use_lowercase: bool = True,
				use_uppercase: bool = True,
				use_digits: bool = True,
				use_symbols: bool = True,
				exclude_ambiguous: bool = True,
				min_lowercase: int = 0,
				min_uppercase: int = 0,
				min_digits: int = 0,
				min_symbols: int = 0) -> str:
		"""
		Generate a secure password

		Args:
			length: Total password length
			use_lowercase: Include lowercase letters
			use_uppercase: Include uppercase letters
			use_digits: Include digits
			use_symbols: Include symbols
			exclude_ambiguous: Exclude characters like i, l, 1, L, o, 0, O
			min_lowercase: Minimum lowercase characters required
			min_uppercase: Minimum uppercase characters required
			min_digits: Minimum digits required
			min_symbols: Minimum symbols required

		Returns:
			str: Generated password
		"""
		# Build character pool
		char_pool = ''
		required_chars = []

		if use_lowercase:
			chars = self.lowercase
			if exclude_ambiguous:
				chars = ''.join(c for c in chars if c not in self.ambiguous)
			char_pool += chars

			# Add required minimum
			for _ in range(min_lowercase):
				required_chars.append(secrets.choice(chars))

		if use_uppercase:
			chars = self.uppercase
			if exclude_ambiguous:
				chars = ''.join(c for c in chars if c not in self.ambiguous)
			char_pool += chars

			for _ in range(min_uppercase):
				required_chars.append(secrets.choice(chars))

		if use_digits:
			chars = self.digits
			if exclude_ambiguous:
				chars = ''.join(c for c in chars if c not in self.ambiguous)
			char_pool += chars

			for _ in range(min_digits):
				required_chars.append(secrets.choice(chars))

		if use_symbols:
			char_pool += self.symbols
			for _ in range(min_symbols):
				required_chars.append(secrets.choice(self.symbols))

		if not char_pool:
			raise ValueError(f"Minimum character requirements ({len(required_chars)}) exceed password length ({length})")

		# Fill remaining length with random characters
		remaining_length = length - len(required_chars)
		password_chars = required_chars + [secrets.choice(char_pool) for _ in range(remaining_length)]

		# Shuffle to avoid predictable patterns
		random.shuffle(password_chars)

		return ''.join(password_chars)

	def generate_passphrase(self, word_count: int = 4, separator: str = '-',
							capitalize: bool = True, add_number: bool = True) -> str:
		"""
		Generate a memorable passphrase (e.g., "Correct-Horse-Battery-Staple")

		Args:
			word_count: Number of words
			separator: Character between words
			capitalize: Capitalize first letter of each word
			add_number: Add number at the end

		Returns:
			str: Generated passphrase
		"""
		# Common word list (you'd normally load this from a file)
		common_words = [
			'able', 'about', 'account', 'acid', 'across', 'addition', 'adjustment',
            'advertisement', 'after', 'again', 'against', 'agreement', 'almost',
            'among', 'amount', 'amusement', 'angle', 'angry', 'animal', 'answer',
            'apparatus', 'apple', 'approval', 'arch', 'argument', 'army', 'attack',
            'attempt', 'attention', 'attraction', 'authority', 'automatic', 'awake',
            'baby', 'back', 'balance', 'ball', 'band', 'base', 'basin', 'basket',
            'bath', 'beautiful', 'because', 'before', 'behavior', 'belief', 'bell',
            'bent', 'berry', 'between', 'bird', 'birth', 'bitter', 'black', 'blade',
            'blood', 'blow', 'blue', 'board', 'boat', 'body', 'boiling', 'bone',
            'book', 'boot', 'bottle', 'brain', 'brake', 'branch', 'brass', 'bread',
            'breath', 'brick', 'bridge', 'bright', 'broken', 'brother', 'brown',
            'brush', 'bucket', 'building', 'bulb', 'burn', 'burst', 'business',
            'butter', 'button', 'canvas', 'card', 'care', 'carriage', 'cart',
            'cause', 'certain', 'chain', 'chalk', 'chance', 'change', 'cheap',
            'cheese', 'chemical', 'chest', 'chief', 'chin', 'church', 'circle',
            'clean', 'clear', 'clock', 'cloth', 'cloud', 'coal', 'coat', 'cold',
            'collar', 'color', 'comb', 'come', 'comfort', 'committee', 'common',
            'company', 'comparison', 'competition', 'complete', 'complex', 'condition',
            'connection', 'conscious', 'control', 'cook', 'copper', 'copy', 'cord',
            'cork', 'cotton', 'cough', 'country', 'cover', 'crack', 'credit', 'crime',
            'cruel', 'crush', 'current', 'curtain', 'curve', 'cushion', 'damage',
            'danger', 'dark', 'daughter', 'decision', 'deep', 'degree', 'delicate',
            'dependent', 'design', 'desire', 'destruction', 'detail', 'development',
            'different', 'digestion', 'direction', 'dirty', 'discovery', 'discussion',
            'disease', 'disgust', 'distance', 'distribution', 'division', 'door',
            'doubt', 'down', 'drain', 'drawer', 'dress', 'drink', 'driving', 'drop',
            'dust', 'early', 'earth', 'east', 'edge', 'education', 'effect', 'elastic',
            'electric', 'engine', 'enough', 'equal', 'error', 'even', 'event', 'ever',
            'every', 'example', 'exchange', 'existence', 'expansion', 'experience',
            'expert', 'face', 'fact', 'fall', 'false', 'family', 'farm', 'father',
            'fear', 'feather', 'feeble', 'feeling', 'female', 'fertile', 'fiction',
            'field', 'fight', 'finger', 'fire', 'first', 'fish', 'fixed', 'flag',
            'flame', 'flat', 'flight', 'floor', 'flower', 'fold', 'food', 'foolish',
            'foot', 'force', 'fork', 'form', 'forward', 'fowl', 'frame', 'free',
            'frequent', 'friend', 'front', 'fruit', 'full', 'future', 'garden',
            'general', 'glass', 'glove', 'goat', 'gold', 'good', 'government', 'grain',
            'grass', 'great', 'green', 'grey', 'grip', 'group', 'growth', 'guide',
            'hair', 'hammer', 'hand', 'hanging', 'happy', 'harbor', 'hard', 'harmony',
            'hate', 'have', 'head', 'healthy', 'hear', 'hearing', 'heart', 'heat',
            'help', 'high', 'history', 'hole', 'hollow', 'hook', 'hope', 'horn',
            'horse', 'hospital', 'hour', 'house', 'humor', 'idea', 'important',
            'impulse', 'increase', 'industry', 'insect', 'instrument', 'insurance',
            'interest', 'invention', 'iron', 'island', 'jelly', 'jewel', 'join',
            'journey', 'judge', 'jump', 'keep', 'kettle', 'kick', 'kind', 'kiss',
            'knee', 'knife', 'knot', 'knowledge', 'land', 'language', 'last', 'late',
            'laugh', 'lead', 'leaf', 'learning', 'leather', 'left', 'letter', 'level',
            'library', 'lift', 'light', 'like', 'limit', 'line', 'linen', 'liquid',
            'list', 'little', 'living', 'lock', 'long', 'look', 'loose', 'loss',
            'loud', 'love', 'machine', 'make', 'male', 'manager', 'mark', 'market',
            'married', 'mass', 'match', 'material', 'meal', 'measure', 'meat',
            'medical', 'meeting', 'memory', 'metal', 'middle', 'military', 'milk',
            'mind', 'mine', 'minute', 'mist', 'mixed', 'money', 'monkey', 'month',
            'moon', 'morning', 'mother', 'motion', 'mountain', 'mouth', 'move',
            'much', 'muscle', 'music', 'nail', 'name', 'narrow', 'nation', 'natural',
            'near', 'necessary', 'neck', 'need', 'needle', 'nerve', 'news', 'night',
            'noise', 'normal', 'north', 'nose', 'note', 'number', 'observation',
            'offer', 'office', 'only', 'open', 'operation', 'opinion', 'opposite',
            'orange', 'order', 'organization', 'ornament', 'other', 'oven', 'over',
            'owner', 'page', 'pain', 'paint', 'paper', 'parallel', 'parcel', 'part',
            'past', 'paste', 'payment', 'peace', 'pencil', 'person', 'physical',
            'picture', 'pipe', 'place', 'plane', 'plant', 'plate', 'play', 'please',
            'pleasure', 'plough', 'pocket', 'point', 'poison', 'polish', 'political',
            'poor', 'porter', 'position', 'possible', 'potato', 'powder', 'power',
            'present', 'price', 'print', 'prison', 'private', 'probable', 'process',
            'produce', 'profit', 'property', 'prose', 'protest', 'public', 'pull',
            'pump', 'punishment', 'purpose', 'push', 'quality', 'question', 'quick',
            'quiet', 'quite', 'rail', 'rain', 'range', 'rate', 'reaction', 'reading',
            'ready', 'reason', 'receipt', 'record', 'regret', 'regular', 'relation',
            'religion', 'representative', 'request', 'respect', 'responsible', 'rest',
            'reward', 'rhythm', 'rice', 'right', 'ring', 'river', 'road', 'roll',
            'roof', 'room', 'root', 'rough', 'round', 'rule', 'safe', 'sail', 'salt',
            'same', 'sand', 'scale', 'school', 'science', 'scissors', 'screw', 'seat',
            'second', 'secret', 'secretary', 'seed', 'seem', 'selection', 'self',
            'send', 'sense', 'separate', 'serious', 'servant', 'shade', 'shake',
            'shame', 'sharp', 'sheep', 'shelf', 'ship', 'shirt', 'shock', 'shoe',
            'short', 'shut', 'side', 'sign', 'silk', 'silver', 'simple', 'sister',
            'size', 'skin', 'skirt', 'sleep', 'slip', 'slope', 'slow', 'small',
            'smash', 'smell', 'smile', 'smoke', 'smooth', 'snake', 'sneeze', 'snow',
            'soap', 'society', 'sock', 'soft', 'solid', 'some', 'song', 'sort',
            'sound', 'soup', 'south', 'space', 'spade', 'special', 'sponge', 'spoon',
            'spring', 'square', 'stage', 'stamp', 'star', 'start', 'statement',
            'station', 'steam', 'steel', 'stem', 'step', 'stick', 'sticky', 'stiff',
            'still', 'stitch', 'stocking', 'stomach', 'stone', 'stop', 'store',
            'story', 'straight', 'strange', 'street', 'stretch', 'strong', 'structure',
            'substance', 'sugar', 'suggestion', 'summer', 'support', 'surprise',
            'sweet', 'swim', 'system', 'table', 'tail', 'take', 'talk', 'tall',
            'taste', 'teaching', 'tendency', 'test', 'than', 'that', 'then', 'theory',
            'there', 'thick', 'thin', 'thing', 'this', 'thought', 'thread', 'throat',
            'through', 'thumb', 'thunder', 'ticket', 'tight', 'till', 'time', 'tired',
            'together', 'tomorrow', 'tongue', 'tooth', 'touch', 'town', 'trade',
            'train', 'transport', 'tray', 'tree', 'trick', 'trouble', 'trousers',
            'true', 'turn', 'twist', 'umbrella', 'under', 'unit', 'value', 'verse',
            'very', 'vessel', 'view', 'violent', 'voice', 'waiting', 'walk', 'wall',
            'war', 'warm', 'wash', 'waste', 'watch', 'water', 'wave', 'weather',
            'week', 'weight', 'well', 'west', 'wheel', 'when', 'where', 'while',
            'whip', 'whistle', 'white', 'wide', 'will', 'wind', 'window', 'wine',
            'wing', 'winter', 'wire', 'wise', 'with', 'woman', 'wood', 'wool',
            'word', 'work', 'worm', 'wound', 'writing', 'wrong', 'year', 'yellow',
            'young'
		]

		# Select random words
		words = [secrets.choice(common_words) for _ in range(word_count)]

		# Capitalize if requested
		if capitalize:
			words = [word.capitalize() for word in words]

		# Jion with separator
		passphrase = separator.join(words)

		# Add number if requested
		if add_number:
			passphrase += str(secrets.randbelow(100))

		return passphrase

	def generate_multiple(self, count: int = 5, **kwargs) -> list:
		"""Generate multiple passwords"""
		return [self.generate(**kwargs) for _ in range(count)]

def main():
	"""Test the password generator"""
	generator = PasswordGenerator()

	print("=" * 70)
	print("PASSWORD GENERATOR TEST")
	print("=" * 70)

	# Test 1: Default password
	print("\n1. Default password (16 chars, all types):")
	print(f"    {generator.generate()}")

	# Test 2: Long password
	print("\n2. Long password (24 chars):")
	print(f"	{generator.generate(length=24)}")

	# Test 3: No symbols
	print("\n3. Password without symbols:")
	print(f"	{generator.generate(use_symbols=False)}")

	# Test 4: Only lowercase and digits
	print("\n4. Only lowercase + digits:")
	print(f"	{generator.generate(use_uppercase=False, use_symbols=False)}")

	# Test 5: with minimum requirements
	print("\n5. With minimum requirements (min 2 of each type):")
	print(f"	{generator.generate(length=20, min_lowercase=2, min_uppercase=2, min_digits=2, min_symbols=2)}")

	# Test 6: Passphrase
	print("\n6. Passphrase (4 words):")
	print(f"	{generator.generate_passphrase()}")

	# Test 7: Multiple passwords
	print("\n7. Generate 5 passwords:")
	passwords = generator.generate_multiple(count=5, length=12)
	for i, pwd in enumerate(passwords, 1):
		print(f"	{i}. {pwd}") 

	print("\n" + "=" * 70)


if __name__ == "__main__":
	main()
	