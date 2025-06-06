# Reproducing *High-performance brain-to-text communication via handwriting*

## Work Log

to track what I do each day

June 5th, 2025
- Downloaded data from https://datadryad.org/dataset/doi:10.5061/dryad.wh70rxwmv#citations.
- Combined all letter data into array of shape (letters, trials, steps, channels).

June 6th, 2025
- Fit a basic PCA model where samples are 192D vectors representing activity for
a particular letter, trial, and time step.
- Plotted the PC1 scores for "d". something looks off. PC1 scores become more negative
for later trials. Update: this was bc I didn't normalize the data! so it makes
sense why there was drift in PC1 scores over time; perhaps baseline firing rates
or variance changed for that same neuron! I learned that each recording "block"
consisted of 3 trials for each character. (about 2.5 minutes, 2s * 3 trials * 26 chars)
- https://snawarhussain.com/blog/neuroscience/PCA-Neural-modes-and-Neural-Manifolds/
- after applying blockwise z-scoring (honestly thank god for his code: https://github.com/fwillett/handwritingBCI/blob/main/matlabExamples/tsneAndKNNExample.m), PC1 looks
consistent across trials for each letter!! not sure if I'm seeing what i want to see
but it does also seem like similarly written letters (e.g. m and n) have similar
PC1 trajectories!
- hmm PC2 and PC3 look less stable across trials tho

