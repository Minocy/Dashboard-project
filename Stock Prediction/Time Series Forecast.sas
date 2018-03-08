ods pdf file='E:\Graduate Studies\Winter\MBAN 6120 Data Science\Project\SASoutput.pdf';
run ;
/*Read the data from Excel File*/
libname tesla pcfiles path=" E:\Graduate Studies\Winter\MBAN 6120 Data Science\Project\Tesla.xls";

proc contents data=tesla._all_;
run;

data work.Tesla;
	set tesla.'Tesla$'n(keep=Day Close);
run; 

proc print data=Tesla(firstobs=1200);
run;

/*Forecasting for the close stock price with Exponential Smoothing technique*/
proc forecast data=Tesla interval=day lead=7
    method=expo weight=0.2 out=out1 outfull outest=est1;
    var Close;
    id Day;
run;

/*Plot the forecasting results against original close price*/
title 'Plot of Forecasts for Tesla Close Price';
proc sgplot data=out1;
     series x=Day y=Close /group=_type_ markers markerattrs=(symbol=circlefilled);
     xaxis values=('02JAN2018'd to '27FEB2018'd);
     refline '20FEB2018'd / axis=x;
run;
title;

/*Print out the data with its forecast from the begining of 2018*/
title ' Forecasting Results of Tesla Stock Price 2018';
proc print data=out1(firstobs=2519);
run; 
title;

ods pdf close; 
run;
