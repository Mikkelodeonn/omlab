% Sets spectrum analyser parameters for ringdown
% Run 'OpenCloseConnection.m' first to initialize the spectrum analyzer
% Run 'RingdownFitAndSave.m' afterwards

SampleName = 'ChamberPressure = 2.8e-4'; ModeName = '(1,1)'; CenterFreq = (702.264e3); AveCount = 100; RBW = 150; SweepTime =40;
%1936.065
FGAmp = 1; %dBm
ChamberPressure = 1.2e-5;  %mbar
% wavelength = str2double(webread('http://10.28.1.116:8000/api/0/'));
% wavelengthString = [strrep( num2str(wavelength, 6 ), '.', '_') 'nm'];
Wavelength = 910.685;       %nm
VDCPZT = 90;                %V
% VdcStr = 1000*str2double(query(refGen, [':VOLT:OFFSET?']));

fprintf(rsa,'DISPlay:GENeral:MEASview:DELete Spec')
fprintf(rsa,'DISPLAY:GENERAL:MEASVIEW:NEW DPX')
fprintf(rsa,'SENSE:DPX:PLOT ZSP')
fprintf(rsa,['SENSE:DPX:TDM:SWEEP:TIME ' num2str(SweepTime)])
fprintf(rsa,['DPX:FREQ:CENTER ' num2str(CenterFreq)]);
fprintf(rsa,['SENSE:DPX:TDM:RBW ' num2str(RBW)]);
fprintf(rsa,['TRACE1:DPX:AVERAGE:COUNT ' num2str(AveCount)]);

fprintf(rsa,['TRACE1:DPX 1']);

% Set trigger signal
TrigFreq=1/SweepTime;
fprintf(FG2,['FREQ:MODE FIXED'])
fprintf(FG2,['FUNC SQU'])
fprintf(FG2,['FREQ ' num2str(TrigFreq)])
fprintf(FG2,['VOLT 2'])
fprintf(FG2,['VOLT:OFFS 1'])
fprintf(FG2, 'OUTPUT:STATE On')

% Set FREQ and AMPL of excitation
fprintf(FG3,['FREQ:MODE FIXED'])
fprintf(FG3,['FUNC SIN'])
fprintf(FG3,['BURST:MODE GATED'])
fprintf(FG3,['BURST:STATE 1'])
fprintf(FG3,['FREQ ' num2str(CenterFreq)])
fprintf(FG3,['VOLT:UNIT DBM'])
fprintf(FG3,['VOLT ' num2str(FGAmp)])
fprintf(FG3, 'OUTPUT:STATE On')

