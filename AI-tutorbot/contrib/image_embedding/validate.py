
import json

from matplotlib import pyplot as plt
import numpy

import torch
from torch import cosine_similarity, pairwise_distance

samples_0 = json.load(open("0-non_augmented.json", 'r'))
samples_1 = json.load(open("1-random_augmented.json", 'r'))

result = [[0 for _ in samples_0] for _ in samples_1]

print("\t" + "\t".join(str(i + 1) for i in range(len(samples_0))))

for i, sample_0 in enumerate(samples_0):
    for j, sample_1 in enumerate(samples_1):
        similarity = cosine_similarity(torch.tensor(sample_0["dense"]).unsqueeze(0), torch.tensor(sample_1["dense"]).unsqueeze(0))
        result[i][j] = round(similarity.item(), 4)

plt.figure()
plt.matshow(result, cmap=plt.get_cmap("Blues"))
plt.xticks(range(len(samples_0)), [i + 1 for i in range(len(samples_1))])
plt.yticks(range(len(samples_1)), [i + 1 for i in range(len(samples_1))])
plt.colorbar()
plt.savefig("temp.jpg")
plt.close()

for i, r in enumerate(result):
    print("{}\t".format(i + 1) + "\t".join(str(element) for element in r))