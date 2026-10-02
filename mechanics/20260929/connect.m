% %% FG1, sigGen %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% % connect Agilent signal generator
% FG1 = instrfind('Type', 'visa-usb', 'RsrcName', 'USB0::0x0957::0x1507::MY48009802::0::INSTR', 'Tag', '');
% 
% % Create the VISA-USB object if it does not exist
% % otherwise use the object that was found.
% if isempty(FG1)
%     FG1 = visa('NI', 'USB0::0x0957::0x1507::MY48009802::0::INSTR');
% else
%     fclose(FG1);
%     FG1 = FG1(1)
% end
% 
% % Connect to instrument object, FG1.
% fopen(FG1);
% 
% fprintf(FG1, 'OUTPUT:STATE Off');
% 
% query(FG1, '*IDN?')
% 
% % query(FG1, 'STAT:QUES:EVEN?')
% % fprintf(FG1, '*CLS')
% % query(FG1, 'STAT:QUES:EVEN?')


%% FG2, refGen %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% connect Agilent signal generator
FG2 = instrfind('Type', 'visa-usb', 'RsrcName', 'USB0::0x0957::0x2507::MY59003466::0::INSTR', 'Tag', '');

% Create the VISA-USB object if it does not exist
% otherwise use the object that was found.
if isempty(FG2)
    FG2 = visa('NI', 'USB::0x0957::0x2507::MY59003466::0::INSTR');
else
    fclose(FG2);
    FG2 = FG2(1)
end

% Connect to instrument object, FG2.
fopen(FG2);
query(FG2, '*IDN?')
fprintf(FG2, 'OUTPUT:STATE Off');

% query(FG2, 'STAT:QUES:EVEN?')
% fprintf(FG2, '*CLS')
% query(FG2, 'STAT:QUES:EVEN?')


%% FG3, sigGen %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% connect Agilent signal generator
FG3 = instrfind('Type', 'visa-usb', 'RsrcName', 'USB0::0x0957::0x2507::MY52102617::0::INSTR', 'Tag', '');

% Create the VISA-USB object if it does not exist
% otherwise use the object that was found.
if isempty(FG3)
    FG3 = visa('NI', 'USB0::0x0957::0x2507::MY52102617::0::INSTR');
else
    fclose(FG3);
    FG3 = FG3(1)
end

% Connect to instrument object, FG3.
fopen(FG3);

fprintf(FG3, 'OUTPUT:STATE Off');

query(FG3, '*IDN?')

% query(FG3, 'STAT:QUES:EVEN?')
% fprintf(FG3, '*CLS')
% query(FG3, 'STAT:QUES:EVEN?')
