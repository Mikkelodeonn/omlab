% This program captures and saves DPX spectrum
% Run 'setSpectrumSettings.m^' first to set the spectrum analyser
% parameters

clear fit_lin  fit_log


SpecTime = now;
datestr(now)

CenterFreq = parameterDouble('SENSE:DPX:FREQ:CENTER?')
Span = parameterDouble('DPX:FREQ:SPAN?');
SetRBW = parameterDouble('SENSE:DPX:BANDWIDTH:RESOLUTION?');
RBW = parameterDouble('SENSE:DPX:BANDWIDTH:ACTUAL?');
AveCount = parameterDouble( 'TRACE1:DPX:AVERAGE:COUNT?');
FreqStart = CenterFreq - Span/2;
FreqStop = CenterFreq + Span/2;
DPXSpec = getDPXSpec(rsa, 1);
dxDPX = linspace(FreqStart * 1e-3, FreqStop*1e-3, length(DPXSpec.Spec));


figure(119); clf
plot(dxDPX, DPXSpec.Spec+2)

hold on
grid on
xlabel('kHz')
ylabel('dBm')
title(['Spec ' SampleName ', Thermal, ' ModeName, ', ' num2str(AveCount) ' Ave, RBW(DPX) ' num2str(SetRBW, 6 ) 'Hz'])
axis tight
legend('Spec')





% if (exist([fname '.mat'], 'file')==2)
% %     error('Filename would overswrite!')
% else
% 
% saveas(119, fname)
% save(fname)
% 
% end

pause(1)
% Fit a Lorentzian curve on the spectrum and finds f and Q

[maxVs,modes] = peakFunc(dxDPX, DPXSpec.Spec, [FreqStart FreqStop]/1000);
NoiseLevel= mean(DPXSpec.Spec(1:round(TracePoints/10)));
pause(0.1)
x= dxDPX';
ydB=(DPXSpec.Spec-NoiseLevel);
y= 10.^(ydB/10);

area = trapz(x,y);


figure(12);clf
f_lin=fittype(@(A,x0,gamma, x) 1+(A ./ (1 +((x-x0)/gamma).^2)) );
f_log=fittype(@(A,x0,gamma, x) 10*log10((1+(A ./ (1 +((x-x0)/gamma).^2)))));
minX = min(x);
maxX = max(x);

% assign initial guessed parameters

pin=[max(y),modes,0.001];

% fit our data
fitobject_lin = fit (x,y, f_lin, 'StartPoint', pin);
fitobject_log = fit (x,ydB, f_log, 'StartPoint', pin,'Lower', [0, minX, 0]);
%how well our fit follows the data
%      plot( x,y)
plot(x,y,'.')
hold on
yfit_lin=fitobject_lin(x);
yfit_log=10.^(fitobject_log(x)/10);

plot(x,yfit_lin,'-r')
plot(x,yfit_log,'-m')
axis tight
hold off

fit_lin.Amp =fitobject_lin.A;
fit_lin.Freq =fitobject_lin.x0;
fit_lin.gamma=fitobject_lin.gamma;
fit_lin.width= 2*fitobject_lin.gamma;
fit_lin.int = integrate(fitobject_lin,maxX,minX);
fit_lin.Q = fitobject_lin.x0./(2*fitobject_lin.gamma);
fit_lin.uncertainty=confint(fitobject_lin,0.950);
fit_lin.AmpE=(fit_lin.uncertainty(2,1)-fit_lin.uncertainty(1,1))/2;
fit_lin.FreqsE=(fit_lin.uncertainty(2,2)-fit_lin.uncertainty(1,2))/2;
fit_lin.gammaE=(fit_lin.uncertainty(2,3)-fit_lin.uncertainty(1,3))/2;
fit_lin.widthE=2*fit_lin.gammaE;
fit_lin.QsE=fit_lin.Q*sqrt((fit_lin.FreqsE/fit_lin.Freq)^2+(fit_lin.gammaE/fitobject_lin.gamma)^2)/2;

fit_log.Amp =fitobject_log.A;
fit_log.Freq =fitobject_log.x0;
fit_log.gamma=fitobject_log.gamma;
fit_log.width= 2*fitobject_log.gamma;
fit_log.int = integrate(fitobject_log,maxX,minX);
fit_log.Q = fitobject_log.x0./(2*fitobject_log.gamma);
fit_log.uncertainty=confint(fitobject_log,0.950);
fit_log.AmpE=(fit_log.uncertainty(2,1)-fit_log.uncertainty(1,1))/2;
fit_log.FreqsE=(fit_log.uncertainty(2,2)-fit_log.uncertainty(1,2))/2;
fit_log.gammaE=(fit_log.uncertainty(2,3)-fit_log.uncertainty(1,3))/2;
fit_log.widthE=2*fit_log.gammaE;
fit_log.QsE=fit_log.Q*sqrt((fit_log.FreqsE/fit_log.Freq)^2+(fit_log.gammaE/fitobject_log.gamma)^2)/2;

%zoom on peak
xlim([fit_log.Freq-10*fit_log.width    fit_log.Freq+10*fit_log.width])


txt0=['Fit in lin scale:'];
txt1=['A = ' num2str(fit_lin.Amp,4) '\pm' num2str(fit_lin.AmpE,2)];
txt2=['w_m = ' num2str(fit_lin.Freq) '\pm' num2str(fit_lin.FreqsE,'%10.0e') ' kHz'];
txt3=['\gamma = ' num2str(fit_lin.gamma*1000,3) '\pm' num2str(fit_lin.gammaE*1000,2) ' Hz'];
txt4=['Q = ' num2str(fit_lin.Q,'%10.3e') '\pm' num2str(fit_lin.QsE,'%10.1e')];

dim = [0.2 0.5 0.3 0.3];
str = {txt0, txt1, txt2, txt3, txt4};
annotation('textbox',dim,'String',str,'FitBoxToText','on');

txt0=['Fit in log scale:'];
txt1=['A = ' num2str(fit_log.Amp,4) '\pm' num2str(fit_log.AmpE,2)];
txt2=['w_m = ' num2str(fit_log.Freq) '\pm' num2str(fit_log.FreqsE,'%10.0e') ' kHz'];
txt3=['\gamma = ' num2str(fit_log.gamma*1000,3) '\pm' num2str(fit_log.gammaE*1000,2) ' Hz'];
txt4=['Q = ' num2str(fit_log.Q,'%10.3e') '\pm' num2str(fit_log.QsE,'%10.1e')];

dim = [0.2 0.2 0.3 0.3];
str = {txt0, txt1, txt2, txt3, txt4};
annotation('textbox',dim,'String',str,'FitBoxToText','on');

xlabel('kHz')
ylabel('Signal(linear)')
title(['Thermal ' SampleName  ModeName, ', ' num2str(CenterFreq) 'Hz,' ...
    num2str(AveCount) 'Ave, RBW' num2str(SetRBW, 6 ) 'Hz'])


fname = ['Thermal ' SampleName  ModeName, ', ' num2str(CenterFreq) 'Hz,'...
     num2str(AveCount) 'Ave, RBW' num2str(SetRBW, 6 ) 'Hz,'  num2str(Wavelength, 6 ) 'nm' ...
     '_' num2str(ChamberPressure, 6 ) 'mbar' '_' num2str(VDCPZT, 6 ) 'Vdc, ' datestr(now)];
fname = strrep(fname, '.', '_');
fname = strrep(fname, ':', '-');
%     fname = ['AlSpacerArray1(1,1)fit' num2str(n) '_RBW' [strrep( num2str(rbw, 6 ), '.', '_') 'Hz']]
% %
% figure(741);hold on
% plot(pres, Q, 'db')

% figure(701);hold on
% plot(ChamberPressure, fitobject.gamma, 'dg')
fit_lin
fit_log

% Construct a questdlg with three options
choice = questdlg('Do you like to save results?', ...
	'Save?','Yes','No','Yes');
% Handle response

txt_filename = fname + ".txt";

switch choice
    case 'Yes'
        % saves MATLAB figure
        save(fname)
        saveas(12, fname)
        % saves raw data file as [idx, frequency, signal]
        file = fopen(txt_filename, 'w');
        for i=1:length(dxDPX)
            fprintf(file, '%f %f\n', dxDPX(i), DPXSpec.Spec(i));
        end
        fclose(file);
end


