clear AmpArray FreqArray QArray

clear fit_lin_array   fit_log_array

AveNo=7;
for i=1:AveNo
   SaveSpecandFitQ
  
   fit_lin_array_A(i)=fit_lin;
   fit_log_array_A(i)=fit_log;
   pause(4)
   
   











end

Amean=mean([fit_lin_array_A(:).Amp]);
Astd=std([fit_lin_array_A(:).Amp]);
Fmean=mean([fit_lin_array_A(:).Freq]);
Fstd=std([fit_lin_array_A(:).Freq]);
Qmean=mean([fit_lin_array_A(:).Q]);
Qstd=std([fit_lin_array_A(:).Q]);

%txt0=['Linear fit data']
%txt1=['A = ' num2str(Amean,4) '\pm' num2str(Astd,2)]
%txt2=['f = ' num2str(Fmean) '\pm' num2str(Fstd,'%10.0e') ' kHz']
%txt3=['Q = ' num2str(Qmean,'%10.3e') '\pm' num2str(Qstd,'%10.1e')]

Amean=mean([fit_log_array_A(:).Amp]);
Astd=std([fit_log_array_A(:).Amp]);
Fmean=mean([fit_log_array_A(:).Freq]);
Fstd=std([fit_log_array_A(:).Freq]);
Qmean=mean([fit_log_array_A(:).Q]);
Qstd=std([fit_log_array_A(:).Q]);
GammaMean= mean([fit_log_array_A(:).gamma]);
GammaSTD=std([fit_log_array_A(:).gamma]);


%txt0=['Log fit data for Membrane']
%txt1=['A = ' num2str(Amean,4) '\pm' num2str(Astd,2)]
%txt2=['f = ' num2str(Fmean) '\pm' num2str(Fstd,'%10.0e') ' kHz']
%txt3=['Q = ' num2str(Qmean,'%10.3e') '\pm' num2str(Qstd,'%10.1e')]
%txt4=['Gamma = ' num2str(GammaMean*1000) '\pm ' num2str(GammaSTD*1000),' Hz']

