




%%

% Tek instruments use port 4000 for their Sockets connections
% We could use VISA, but using sockets means we don't need to
% install VISA software
TekPort = 4000;
maxRetries = 100;
maxDots = 20;

%IPAddress = '10.28.1.122'

IPAddress = '169.254.128.249' % Autoconfiguration IPv4 Address -> used for direct ethernet connection

%IPAddress = 'RSA5103BB040641.phys.st.lab.au.dk'

format compact

% Find and close any open connections
openConnections = instrfind('Tag','TekRSA6K_AcquireIQData');
if ~isempty(openConnections)
    fclose(openConnections(:));
end

% Create TCPIP Object set it up and open connection
global rsa;
rsa = tcpip(IPAddress,TekPort);
rsa.InputBufferSize = 50e6;
rsa.Tag = 'TekRSA6K_AcquireIQData';
rsa.Timeout = 3;                    % set timeout to 3 seconds
rsa.ByteOrder = 'littleEndian';     % Instrument returns data in littleEndian format
warning('on','instrument:query:unsuccessfulRead') % anr was off 
fopen(rsa);

% Reset the instrument and query it
%fprintf(rsa,'*RST;*CLS');

instrumentID = query(rsa,'*IDN?')
if isempty(instrumentID)
    throw(MException('RSAIQCapture:ConnectionError','Unable to connect to instrument'));
end
disp(['Connected to: ' instrumentID]);

% Get number of IDs
IDDetails = query(rsa,'FETCh:RFIN:RECord:IDS?');
IDFields = regexp(IDDetails, ',', 'split');
count = 0;
while ~isequal(length(IDFields),2)
    IDdetails = query(rsa,'FETCh:RFIN:RECord:IDS?');
    IDFields = regexp(IDDetails, ',', 'split');
    count = count + 1;
    if count>maxRetries
        throw(MException('RSAIQCapture:IDError', sprintf('Unable to obtain number of record ID''s from the instrument after %d tries.',count)));
    end
end


%%
% 
% 
% fclose(rsa);
%clear('rsa')
