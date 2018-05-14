


The primary goal of this package is to help in the analysis of a chord progression and facilitate learning of jazz standards.  
It will also suggest alternative chords, progressions, scales etc     
For example, we can enter a progression as a string, ask to analyse then plot the results.   
Each cell shows the chord, its degree in the corresponding scale, and optionally the coresponding notes.  
Right know we are only searching for ionian II-V-I, II-V and V-I, but the plan is to extend to other progressions.  

[Basic Examples](https://github.com/NeuralControl/jazzTheory/blob/master/demos.ipynb)  

From a chord progression, we can analyze and plot the results:
```python
prg = Progression('|Dm7,G7|Dm7,G7|Em7,A7|Em7,A7|Am7,D7|Abm7,Db7|CM7|CM7|',name='Satin Doll')  
prg.analyze()  
prg.plot()  
```
![SatinDoll](img/SatinDoll.png)  


Plot all Chords in a given Scale:  
```python
Scale('C minor').plotChords()
```
![SatinDoll](img/allChords.png)  

Plot all m7 for all roots:  

![SatinDoll](img/allKeys.png)  

Plot implemented chords:  
![SatinDoll](img/ImplementedChords.png)

