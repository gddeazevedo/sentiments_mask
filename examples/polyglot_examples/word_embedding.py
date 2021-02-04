import os
from polyglot.mapping import Embedding



HOME = os.environ['HOME']

path = f'{HOME}/polyglot_data/embeddings2/pt/embeddings_pkl.tar.bz2'

embeddings = Embedding.load(path)
neighbors = embeddings.nearest_neighbors('amor')

print(neighbors)
print(embeddings.distances('amor', neighbors))