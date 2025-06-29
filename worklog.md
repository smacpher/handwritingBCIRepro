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


June 10th, 2025
- so i think what I missed is that they fit the PCA on trial-averaged activity,
the idea being that this will result in more stable PCs that aren't fit on noise;
so they first fit the PCA on trial-averaged data then project the single-trial
activity on the PCs; hopefully this will reproduce their charts; time to learn
about Guassian smoothing (the technique they use to average data across trials)...
- Guassian smoothing
  - reading this: https://matthew-brett.github.io/teaching/smoothing_intro.html
  - notes:
    - why smooth? increase signal-to-noise ratio

- ok so the steps willet's takes before PCA:
 1. blockwise z-score for each trial's data (three trials per block for each letter, so block
 contains 3 * 26 = 78 trials)
 2. takes the mean of the trials for the letter as the activity for that letter
 3. applies a causal (only uses past time steps in weighted average smoothing step)
 gaussian smoothing
- very cool so the PCs now look more similar to Willet's after just fitting them
on the trial-averaged activity then projecting per-trial activity onto each! so
could show the importance of each of these preprocessing steps to detrend /
denoise data in my presentation; i think the intuition behind why PC1 still
looked okay before taking trial-mean is that its less suscetible to noise, tells
us that signal dominates noise in the first dimension of its variance but then
in dimensions with less variation, noise competes with signal
- i was also able to reproduce the guassian smoothing thanks to chatGPT; the
figure looks damn close to willet's if not identical; still need to dig into how 
gaussian smoothing / the code works
- it would be cool to show a visual behind the intuition of dimensionality
reduction in neural data to show "Population of neurons confining their activity into a lower dimensional manifold within the high N-dimensional space due to interconnectivity" from
https://snawarhussain.com/blog/neuroscience/PCA-Neural-modes-and-Neural-Manifolds/

- open questions:
  - how did he decide on the width of the Gaussian smoothing kernel? is this
  convention for intrasubject microelectrode neural activity? why do we use a
  wider kernel (width=5) for trial-averaged data, but a narrower one for the
  per-trial data (width=3)?

- random:
  - found course notes for analyzing fMRI data: https://textbook.nipraxis.org/intro.html

- would be interesting to visualize activity of neurons before and after
  SSRIs; why do SSRIs often "blunt" the extreme ends of emotions? or doing the
  same for ketamine; is it actually "activating" (increasing firing rates or
  synchrony) certain populations of neurons?

June 11th, 2025
- goals for this ~1 hour session: i want to familiarize myself better with
obsidian; eventually, it would be cool to have a setup that serves as a second
brain where I can track all that I learn as I dig into BCI research. So much
spiderwebs out of a single paper; for example, just in the first section of the
willets handwriting bci paper, I'm already googling things like Gaussian smoothing,
pca, t-sne, blockwise z-scoring, etc. It would be great to start building up
a sort of mini wikipedia of concepts described in my own words that i can
go back to.
- stretch goal: takes notes on time-warping technique

June 12th, 2025
- read through https://pubmed.ncbi.nlm.nih.gov/37201504/ "Discovering Precise Temporal Patterns in Large-Scale Neural Recordings through Robust and Interpretable Time Warping" and wrote
a summary in Obsidian; really cool paper. Love the simplicity of the technique
- going to try to use affinewarp on one character's data and play around with that; maybe
I can try to display a line chart (not heatmap) of the PCs of that char's activity before and after
warping to hopefully see that the warped activity is more aligned. willet's used
the authors' old package, twPCA, so can fall back to that if needed

June 13th, 2025
- trying affinewarp shift-only first - so just shifting the entire trial by a fixed
amount (changing the y-intercept of an identity warping function), no stretching
or compressing
- so for each character, willet's preprocesses with: blockwise z-scoring, gaussian
smoothing, then fits a twPCA to fit a warping function / template time series
across all trials. Does this not overfit to that character's activity? Don't we
only want to learn variations in timing across trials, not necessarily variations
in timing across characters...the latter will fit on the specific timings associated
with writing a specific character, idk. What would happen if we fit a warping function per block-so including a few trials from all the characters?
- so to reproduce this in affinewarp, I see two approaches:
  - time warp each character first, then fit PCA over all warped trials
  - do the reverse: fit PCA over trial-averaged activity, then time warp over
  projected single-trial activity
- why do PC2 and PC3 seem less aligned before time warping than PC1?

June 15th, 2025
- goal: visualized warped trials for one character and confirm that activity
is more aligned after warping
  - first approach: fit a simple shift warping function for "d" then use the
  PCA fit on trial-averaged activity to project the warped trajectories for
  d in 3D...didn't seem to align neural trajectories for PC1...maybe b/c
  the shift warping function didn't de-jitter the data enough, or bc the PCA
  was fit on the averaged, jittered (so more squashed out version of the actual
  activity) data...

June 16th, 2025
- goal: figure out what hyperparams reproduce twPCA's behavior in affinewarp
  - okay: not sure I have the time to reproduce twPCA in affinewarp – it's unclear
  which hp's map to what and how many knots are being used in twPCA
  - going to pivot to trying to get twPCA working; will need to setup a new
  virtualenv with python3.7 though
- trying to fit PiecewiseWarping models on each char using n_knots=5 and the
same smoothness and warp reg scale that willet's uses in twPCA (not sure if
they mean the exact same thing tho); so I fit the warp models on smoothed data,
fitting on raw data showed no improvement in loss + willet's says this is key
in the twPCA code. I then transformed the raw data to align it, then smoothed it.
I fit a PCA using the smoothed, trial-average, aligned data but when I projected
the smoothed, per-trial, aligned data using said PCA, the heatmaps were very
smudgey...trying again with n_knots=n_timesteps
  - n_knots=201 (n_timesteps) seemed to jitter the data even more...
  - trying again with 1000 training iters...ok that didn't work either
- it's time to focus all my efforts on getting twPCA to work
  - tried to install tf v1.15 using Rosetta + conda + python3.7 and tf crashed
  on import with "illegal hardware instruction"; next i'll try running it in
  a docker container

June 28th, 2025 Update
- i stopped logging my work for some reason

