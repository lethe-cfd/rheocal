# rheocal
The rheocal project aims at developing a simple tool to automatically calibrate rheological models for generalized newtonian fluids based on experimental viscosity measurements.

## User guide
Here are the steps to follow to obtain the nonlinear regression for a rheology model. The program currently offers nonlinear regression for the following rheology models: Power Law, Carreau, Cross. 
When running the rheocal.py program, the user interface will pop up. This window can be resized or minimized.

### 1. Input file format
The **"Help" tab** is by default the first tab opened. It shows a picture of how data should be entered in the input file in order for the program to execute properly. 

The file must contain two columns:
- shear rate values on the <ins>left</ins>
- viscosity values on the <ins>right</ins>

There must be **no header** and the **period is used for decimal separator.**

### 2. Select an input file
Click on the **"Input" tab** and then click on the **"Browse file" button** to select a file. On the pop-up window, you may then select a **.txt** or **.csv (comma separated format)** file from your directories. 

Once the file is selected, the name of the file will show up in the empty space at the top (see picture) and a frame on the right will show a graph of the entered data on a logarithmic scale. If the wrong file updloaded, or if the is a change to make, another file can be selected instead by direclty using the **"Browse file" button** again.

note: the file does not have to be in the current directory

### 3. Selecting a rheology model
If the input file name and the input data graph show up correctly, you may then select a rheology model by opening the **dropown menu** (default model is the Power Law model). Once you have selected, click the **"Ok" button**.

* **Once selected, the rheology model <ins>cannot be changed!</ins>**

The equation of the selected model will show up in a frame below. 

### 4. Entering guess values
Guess values can be entered in the white boxes. For Cross and Carreau models, the default value for &#951;_0 is max(&#951;) and &#951;_inf is min(&#951;). These values can be changed. For the regression to function properly, all the entry box must contain a numerical value, with dot as decimal separator if needed.

The **"Show me my guess" button** will plot on the graph what the model would look like with the guess. The input data from the selected file will also show and the user may correct the guess and click to visualize again until it is close enough to the input file. The guesses must be <ins>**very close**</ins> to the real values. the <ins>transition should be about right</ins> by the eye. 

* If any non-numerical value is entered, an error message will be printed and the **<ins>user will have to restart the program.</ins>**
* The "Show me my guess" button **<ins>must be activated at least once</ins>** in order to run the regression

### 5. Running the regression and reading results
Once the initial values are guessed by user and the **"Show me my guess" button** has been pushed at least once, clicking on the **"Run" button** will start the regression. Shortly, the values found by the software should appear in the input tab, on the bottom left frame (Results). For more details on the results, the **"Results" tab** to show the performance report. The regression will also be plotted on that tab against the input values. The number of iterations needed, the tolerance obtained, the R square coefficient and the average error in percentage are displayed on the right. The toolbar below the graphs allows to save, reconfigure and zoom in on the subplot. 


## Roadmap
Here are some components of the software to improve in the next steps. They are listed from most relevant to least important. Components 5 or more are challenges or nice to have.

#### 1. Stronger solver
A first improvement would be the nonlinear solver. On the current version, the initial guesses must be too precise to correctly perform the regression, which might in some case defeat the purpose of the software. The current method for solving the relative least square sum is the Newton-Raphson method with a numerical jacobian matrix and variable relaxation. 

The module ```scipy.optimze``` was also briefly tested. The functions ```scipy.optimze.minimize``` (minimize the least square sum), ```scipy.optimze.least_squares``` and ```scipy.optimze.fsolve``` (solve the nonlinear system) were tested, but the resulting solver was not enough performant. 

#### 2. Detailed performance report
The performance report is very brief in the current version. However, the R squared coefficient is a poor method of evaluating the regression quality. Hence the need for more statistical evaluations of the regression. For example, the report could include the p values.

#### 3. Flexible inputs
The current interface does not allow the user to make many changes in the inputs. Here are some downsides that would be good to fix:
1) Change the selected model: with the current version, it is impossible to change model once it has been selected with the "Ok" button. This might not be hard to fix, the variables can be cleaned easily. However ont the previous attempts, the interface could not be completely cleared of the widgets.
2) Rerun the program: It would be more practical not to have to close the file and rerun the program everytime the user wants to evaluate another set of data.
3) "Show me my guess" to save guesses: another graphic user interface issue - the user's guesses are save only when this button is clicked to pass the variables correctly
4) Non-numeric entries: Non-numeric entries in the input file and the guess causes the end of the program. It would be usefull to add a function to allow to re-enter inputs.
5) Input files: it would be relevant to allow a header to the input files, and perhaps to read the data based on these headers.


#### 4. Warning and error messages
It would be usefull to show the sources of problems on the user interfaces. It would be very helpful to identify whether the problem lies in the software and the use of rheocal, or in the input data. 
Relevant warnings include:
1) Irrealistic inputs: too many outliers, odd range of values
2) Maximum iteration used: If the regression ended because the maximum number of iteration was used, a good thing would be to send the user some information as to what happened. This information might include the residual matrix, the last few steps on the parameters or the relaxation factors to indicate if the solution has converged.
3) Initial guesses quality: it might be helpful to inform the user of the quality of the guesses. It could be based for example on the mean relative error and show a warning if it is too low.


#### 5. Impose one or multiple parameters
If the user has a better idea of the expected answer, it would be nice to be able to impose a value on one or multiple parameters. But if there is one less variable parameter, the nonlinear equation systems goes from n equations to n-1 equation, meaning the whole problem is changed. It might not be hard to implement, since it would simplify the mathematical problem, but it would probably be time consuming and require good code architecture. 


#### 6. Guess function for initial values:
A guess function, that could run either optionally or automatically to display default values, would help the user find a realistic range on the initial parameter values. This is might be the most difficult function to implement, because the regression might or might not converge, depending on these values. Hence why it might be preferable to let the user modify the values guessed by this function.

The parameters can vary widely depending on the fluid. But here are some observations to help:
- Power law model: on a logarithmic graph, n corresponds to the slope of the line, while m corresponds to the y intercept on the regression line.
- Carreau model: at the first inflection of the curve (on the left), the shear rate value is about equal to 1/&#955;.
The n parameter is also directly linked to the slope of the line.


#### 7. Autofit function
When the user doesn't know which rheology model would best describe a set of data, the autofit function would try each model. Then, based on the performance reporte, the user report would be able to see which model has the best performance for different statistical parameters. Ideally, the user could ask to be showed first the best model based on a parameter of his choosing. The parameter, such as the R squared value or the mean error, would then be one of the input of the regression.

It would be very helpful for this to have a guess function, otherwise the user would also have to select initial values for all parameters of all the models available. Another solution would be to offer the user to compare two models (or more) , instead of trying them all.


#### 8. Carreau-Yasuda model:
For some fluids, the [Carreau-Yasuda model](https://lethe-cfd.github.io/lethe/theory/fluid_dynamics/rheology.html), which has one more parameter than the Carreau model, would best describe the result. 
The regression with 5 parameters has not been attempted yet with a minimum relative squared error problem and variable relaxation. 


#### 9. One function to print all graphs
All the graphs have the same format, but are called with their own canvas and on different frames. It is probably possible to create a function that takes the plotted data, frame and canvas and shows the three different graphs. It was not implemented in this version because it required a lot of time and debugging with the GUI modules.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Authors
##### Main developper 
Bérénice Dubois

##### Contributors
Bruno Blais
