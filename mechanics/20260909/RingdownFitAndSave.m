%% get ringdown


% fs = dir(['R*_' sampleName '*.mat'])
% NNs = zeros(1,size(fs,1));
% for n=1:size(fs,1)
%     prf = split(fs(n).name, '_');
%     NNs(n) = str2num(prf{1}(2:end));
% end
% sort(NNs)
% Nf = max(NNs) + 1;
% 
% if (isempty(fs))
%     Nf = 1;
% end

% Nf = 3

% fprintf(rsa, '*CLS')
% fprintf(rsa,'ABORt;INITiate:IMMediate;*OPC')
% pause(1)

stat = str2double(query(rsa, 'STATUS:OPER:COND?'));
%%%%%%%%%%%%%%
 while isnan(stat)
     
     disp('Waiting for RSA');
     pause(5);
%      stat = str2double(query(rsa, 'STATUS:OPER:COND?'))
%      fprintf(rsa,'ABORt;INITiate:IMMediate;*OPC')
%      fprintf(rsa, '*CLS')
 end
%%%%%%%%%%%%%%%%%%%%%
fprintf(rsa,['FETCh:DPX:RESults:TRACe1?']);
DPXresults = binblockread(rsa,'single');
     linRingdown = 10.^(DPXresults/10);
ringdown = DPXresults;
ringdown = ringdown(ringdown>-1000);

% CenterFreq = str2double(query(refGen,'SOURCE:FREQ?'));
CenterFreq = parameterDouble( 'SENSE:DPX:FREQ:CENT?');
Freq = CenterFreq;
AveCount = parameterDouble( 'TRACE1:DPX:AVERAGE:COUNT?');

% actual bandwidth / acquisition bandwidth
acqBandwidth = parameterDouble( 'SENSE:ACQuisition:BAND?');

% acquisition length
acqTime = parameterDouble( 'SENSE:ACQuisition:SEConds?');

% DPX TDM rbw
RBW = parameterDouble( 'SENSE:DPX:TDM:BAND:ACT?');
centerFreq = parameterDouble('SENSE:DPX:FREQ:CENT?');
span = parameterDouble( 'SENSE:DPX:FREQ:SPAN?');


%doesnt work
% dpxAv = parameterDouble( 'TRACE1:DPX:AVERAGE:COUNT?')

% dsoRepPeriod = str2double(query(dso, 'WGEN:PERIOD?'));



% systemTime = parameterDouble( 'SYSTEM:TIME?')

sweepTime = parameterDouble( 'SENSE:DPX:TDM:SWEEP:TIME?');


t = linspace(0, sweepTime*1e3, size(ringdown,1));

figure(201);clf;hold on
plot(t, ringdown, '.-');

grid on
xlabel('Time [ms]');
ylabel('Intensity [dBm]');

% drive parameters
%it is connected through a 15 dB attenuator

% fprintf(refGen, ['VOLT:UNIT VPP'])
% driveAmplitude = str2double(query(newGen, 'VOLT?'))
% driveFrequency = str2double(query(newGen, 'FREQ?'))

% pump parameters

% fprintf(rsGen, ['VOLT:UNIT VPP'])
% pumpAmplitude = str2double(query(rsGen, 'LEVEL?'))
% pumpFrequency = str2double(query(rsGen, 'FREQ?'))


% set before 
% % driveFrequency = rf3.getFrequency
% drivePower = rf.getPower(2)
% pumpPower = rf.getPower(3)
% drivePhase = rf.getPhase(2);
% pumpPhase = rf.getPhase(3);
%pumpFrequency = 2*driveFrequency
%fprintf(rsGen,['FREQ ' num2str(pumpFrequency)])



%% specifying the time range used for the fit
if true
    figure(201);
    dcm_obj = datacursormode(201);
    datacursormode on
    
    c_info = getCursorInfo(dcm_obj);
    while numel(c_info)<2
     pause(1)
     c_info = getCursorInfo(dcm_obj);
    end
    xp1 = c_info(1).Position(1);    
      xp2 = c_info(2).Position(1);
    
    datacursormode off
    minx = min([xp1 xp2]);
    maxx = max([xp1 xp2]);
    
    ind = find(t>minx & t<maxx);
end

%
% % 

f = fit(t(ind)', ringdown(ind), 'poly1');

ylim1 = ylim;

plot(t(ind), ringdown(ind), 'm-')

plot(t(ind), feval(f, t(ind)), 'g-','LineWidth',3)
%     plot(f, 'g-')

ylim(ylim1);

title(['Ringdown ' SampleName  ModeName, ', ' num2str(CenterFreq) 'Hz, ' num2str(AveCount) ...
    ' Ave, RBW ' num2str(RBW,3) 'Hz']);

figure(203);clf; hold on; grid on

plot(t(ind), 10.^(ringdown(ind)/10), 'r-')
plot(t(ind), 10.^(f.p1*t(ind) / 10 + f.p2/10))
ylabel('Intensity [mW]')
xlabel('Time [ms]')


fexp = fit(t(ind)', 10.^(f.p1*t(ind) / 10 + f.p2/10)', 'exp1');
num2str(Freq*1e-3);
tau = -2/fexp.b;

Q = pi*Freq*(tau*1e-3)
% 
% % Gamma = 2/(tau*1e-3)

% Df = (2*Freq)/(Gamma)
title('Ringdown fitted.');

% remove annotation and fit lines from figure 201
if false
    figure(201);
    h = gcf;
    axesObjs = get(h, 'Children');
    dataObjs = get(axesObjs, 'Children');
    figLineGreen = dataObjs(1);
    figLinePurple = dataObjs(2);
    delete(figLineGreen);
    delete(figLinePurple);
    delete(findall(gcf,'Tag','AnnotationTextQ'))
    clear('h')
    
end

%

annotationText = ['\tau_c ~ ' num2str(round(tau)) ' ms, Q ~ ' num2str(round(Q),3) ...
    ];
figure(201);
annotation(figure(201),'textbox',...
    [0.166 0.1799 0.567928571428571 0.064],...
    'String',annotationText,'LineStyle','none',...
    'FitBoxToText','off', 'Tag', 'AnnotationTextQ');

%

% savenumber
% Nf = Nf + 1;

if false
    while true
        runner
    end
end

%
% pres = 3.4e-5;
% presName = strrep(strrep( num2str(pres, '%1.1e' ), '.', '_'), '-', '_');

% p1 = ssh2_simple_command('raompi.phys.st.lab.au.dk',...
%         'pi', 'Lam397nm','tail -n 1 PressureReading/pressureLog.txt');
% p1s = strsplit(p1{1});
% pressure= str2double(p1s{3});

% presName = strrep(strrep( num2str(pressure, '%1.1e' ), '.', '_'), '-', '_');

% wavelength = getStableWavelength();

% wavelength = str2double(webread('http://10.28.1.116:8000/api/0/'));
% % '%1.3e'
% wavelengthString = [strrep( num2str(wavelength, 6 ), '.', '_') 'nm'];


fname = ['Ringdown ' SampleName  ModeName ', ' num2str(CenterFreq) 'Hz, '...
     num2str(AveCount) 'Ave, RBW' num2str(RBW, 3 ) 'Hz, ' num2str(Wavelength, 6 ) 'nm' ...
     '_' num2str(ChamberPressure, 6 ) 'mbar' '_' num2str(VDCPZT, 6 ) 'Vdc, ' datestr(now)];


% VdcStr = 1000*str2double(query(refGen, [':VOLT:OFFSET?']));

fname = strrep(fname, '.', '-');
fname = strrep(fname, ':', '-');

txt_filename = fname + ".txt";

% Construct a questdlg with three options
choice = questdlg('Do you like to save results?', ...
	'Save?','Yes','No','Yes');
% Handle response
switch choice
    case 'Yes'
        save(fname)
        saveas(201, fname)
        % saves raw data file as [time, intensity]
        file = fopen(txt_filename, 'w');
        for i=1:length(t)
            fprintf(file, '%f %f\n', t(i), ringdown(i));
        end
        fclose(file);
end


% ready for reoptimization
% trigger free run
% fprintf(rsa, 'TRIGGER:SEQ:STATUS 0');
% query(rsa, 'TRIGGER:SEQ:STATUS?')

% fprintf(refGen, 'BM:STAT OFF')
