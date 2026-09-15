% Sets spectrum analyser parameters
% Run 'OpenCloseConnection.m' first to initialize the spectrum analyzer
% (rsa)
FreqA = 703.814e3;
0
i = 1;
j = 1;
FreqX=(((j^2+i^2)/2)^0.5)*FreqA
%SampleName = 'PE_01'; ModeName = '(1,1)'; CenterFreq =sqrt(5)*(835.6e3)/sqrt(1); Span =5000; AveCount =30; RBW = .1;
%SampleName = 'O_test'; ModeName = '(1,1)'; CenterFreq =sqrt(2)*800.65e3; Span =200000; AveCount =100; RBW = .1;
%SampleName = 'O_test'; ModeName = '(2,1)'; CenterFreq =1287.978e3; Span =300; AveCount =100; RBW = 0.1;
%SampleName = 'O_test'; ModeName = '(1,1)'; CenterFreq =799.199e3; Span =10000; AveCount =100; RBW = .1;
SampleName = 'PCS 02'; ModeName = '(1,1)'; CenterFreq =FreqX; Span =100; AveCount = 100; RBW = 0.1;
%at 62-64 volt

%2457.433 2481.111, 2492.365 , *1853.5361 ,1854.233, *1854,474 ,1854.704, *1866.781 1890.579 60 volt5

TracePoints = 10401;
ChamberPressure =170;  %mbar
% wavelength = str2double(webread('http://10.28.1.116:8000/api/0/'));
% wavelengthString = [strrep( num2str(wavelength, 6 ), '.', '_') 'nm'];
Wavelength = 900.700;       %nm
VDCPZT = 0;                %V
% VdcStr = 1000*str2double(query(refGen, [':VOLT:OFFSET?']));

% Stop Excitation
% fprintf(FG3,'OUTPUT:STATE Off')

fprintf(rsa,'SENSE:DPX:PLOT SPEC')
fprintf(rsa,['DPX:FREQ:CENTER ' num2str(CenterFreq)]);
fprintf(rsa,['DPX:FREQ:SPAN ' num2str(Span)]);
fprintf(rsa,['DPX:BANDWIDTH:RESOLUTION ' num2str(RBW)]);
fprintf(rsa,['TRACE1:DPX:AVERAGE:COUNT ' num2str(AveCount)]);
fprintf(rsa,['DPX:POINts:COUNt p' num2str(TracePoints)])

% bw =  str2double(query(rsa,'SPEC:BAND?'));

fprintf(rsa, 'SPEc:BAND:VID 1')
% vbw = str2double(query(rsa,'SPEC:BAND:VID?'));



% freqStart = centerFreq - span/2;
% freqStop = centerFreq + span/2;
% 
% fprintf(rsa,['SPEC:FREQ:START ' num2str(freqStart)]);
% fprintf(rsa,['SPEC:FREQ:STOP ' num2str(freqStop)]);
% 
% freqStart = str2double(query(rsa,'SPEC:FREQ:START?'))
% 
% freqStop = str2double(query(rsa,'SPEC:FREQ:STOP?'))

fprintf(rsa,['FETCh:SPEC:TRAC1?']);
% trace1 = binblockread(rsa,'single');



%fclose(rsa);
